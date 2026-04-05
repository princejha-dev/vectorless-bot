import json
import time
from src.client import pi_client, groq_client, DOC_ID


def llm_generate(prompt: str) -> str:
    """Call Groq LLM with retry for rate limits."""
    for attempt in range(3):
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                print(f"⏳ Rate limited, retrying in 25s... (attempt {attempt + 1})")
                time.sleep(25)
            else:
                raise
    return ""

# ── Step 1: Load the tree (cached after first call) ─────────────────────────
_tree_cache = None

def get_tree():
    """Fetch the document tree from PageIndex (cached)."""
    global _tree_cache
    if _tree_cache is None:
        result = pi_client.get_tree(DOC_ID, node_summary=True)
        _tree_cache = result.get("result", [])
    return _tree_cache


# ── Step 2: LLM Tree Search — picks relevant nodes ──────────────────────────
def llm_tree_search(query: str, tree: list) -> list:
    """Send query + tree to Groq, get back relevant node_ids."""

    def compress(nodes):
        out = []
        for n in nodes:
            entry = {
                "node_id": n["node_id"],
                "title": n["title"],
                "page": n.get("page_index", "?"),
                "summary": n.get("text", "")[:150],
            }
            if n.get("nodes"):
                entry["children"] = compress(n["nodes"])
            out.append(entry)
        return out

    prompt = f"""You are a student academic assistant. You are given a student's query and the tree structure of the Academic Regulations 2025 document.
Your task: identify which node IDs most likely contain the answer to the student's query.
Think step-by-step about which sections/regulations are relevant.

Student Query: {query}

Document Tree:
{json.dumps(compress(tree), indent=2)}

Reply ONLY in this exact JSON format:
{{
  "thinking": "<your step-by-step reasoning>",
  "node_list": ["node_id1", "node_id2"]
}}"""

    text = llm_generate(prompt).strip()
    # Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]

    result = json.loads(text)
    return result.get("node_list", [])


# ── Step 3: Find nodes by their IDs ─────────────────────────────────────────
def find_nodes_by_ids(tree: list, target_ids: list) -> list:
    """Recursively walk the tree and collect nodes matching target_ids."""
    found = []
    for node in tree:
        if node["node_id"] in target_ids:
            found.append(node)
        if node.get("nodes"):
            found.extend(find_nodes_by_ids(node["nodes"], target_ids))
    return found


# ── Step 4: Generate answer using retrieved context ──────────────────────────
def generate_answer(query: str, nodes: list) -> str:
    """Takes retrieved nodes as context and generates a grounded answer."""
    if not nodes:
        return "⚠️ No relevant sections found in the Academic Regulations."

    # Build context from retrieved nodes
    context_parts = []
    for node in nodes:
        context_parts.append(
            f"[Section: '{node['title']}' | Page {node.get('page_index', '?')}]\n"
            f"{node.get('text', 'Content not available.')}"
        )
    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a helpful student academic assistant specializing in Academic Regulations 2025.
Answer the student's question using ONLY the provided context from the regulations document.
For every claim, cite the section title and page number in parentheses.
Be clear, concise, and student-friendly. If the answer involves steps or procedures, use numbered lists.

Student Question: {query}

Context from Academic Regulations:
{context}

Answer:"""

    return llm_generate(prompt)


# ── Main function: Full RAG Pipeline ─────────────────────────────────────────
def ask_question(question: str) -> str:
    """
    Full Vectorless RAG pipeline:
    1. LLM Tree Search → finds relevant node_ids
    2. Node Retrieval  → fetches section content
    3. Answer Generation → produces cited answer
    """
    try:
        tree = get_tree()
        node_ids = llm_tree_search(question, tree)
        nodes = find_nodes_by_ids(tree, node_ids)
        answer = generate_answer(question, nodes)
        return answer
    except Exception as e:
        return f"❌ Error: {str(e)}"

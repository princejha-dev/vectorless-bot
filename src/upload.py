import time
from src.client import pi_client

pdf_path = "./ACADEMIC REGULATIONS 2025.pdf"

document = pi_client.submit_document(pdf_path)
doc_id = document['doc_id']

print(f"doc id of the document is {doc_id}")


print("⏳ Building tree index...")

while True:
    status_result = pi_client.get_document(doc_id)
    status = status_result.get("status")
    print(f"   Status: {status}")
    
    if status == "completed":
        print("\n✅ Tree index ready!")
        break
    elif status == "failed":
        print("\n❌ Processing failed. Check your PDF format.")
        break
    
    time.sleep(5)
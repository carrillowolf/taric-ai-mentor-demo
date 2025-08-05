import os, pandas as pd
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()  # Carga las variables AZURE_DOC_INTEL_ENDPOINT, etc.

client = DocumentAnalysisClient(
    endpoint=os.getenv("AZURE_DOC_INTEL_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_DOC_INTEL_KEY")),
)

MODEL_ID = os.getenv("MODEL_ID")

def parse_invoice(path: str) -> pd.DataFrame:
    """Devuelve un DataFrame con descripción, cantidad, valor, país."""
    poller = client.begin_analyze_document(MODEL_ID, document=open(path, "rb"))
    result = poller.result()

    items = result.documents[0].fields["Items"].value
    rows = []
    for it in items:
        f = it.value
        rows.append(
            dict(
                descripcion=f["Description"].content.strip(),
                cantidad=f.get("Quantity", {}).get("content", ""),
                valor=f.get("Amount", {}).get("content", ""),
                pais=f.get("CountryOfOrigin", {}).get("content", ""),
            )
        )
    return pd.DataFrame(rows)

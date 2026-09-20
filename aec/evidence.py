"""Local extractive evidence retrieval. No LLM call and no claim of generative AI."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

POLICIES=[
 {'id':'CTRL-01','text':'Order authorisation requires an approved requisition, a named budget owner and recorded approval. The requester cannot approve their own purchase order.'},
 {'id':'CTRL-02','text':'Invoice matching compares invoice quantities and rates with the purchase order and goods receipt. Payment remains on hold when matching exceptions are unresolved.'},
 {'id':'CTRL-03','text':'Variation approval requires a scope description, estimated cost, evidence and delegated commercial approval before budget changes are posted.'},
 {'id':'CTRL-04','text':'UAT exit requires all critical scenarios passed, no unresolved critical defects, reconciled migration balances and signed business acceptance.'},
 {'id':'CTRL-05','text':'Supplier delivery risk scores support procurement follow-up only. A buyer must verify current supplier commitments before taking action.'},
 {'id':'CTRL-06','text':'Synthetic cost forecasts depend on assumed physical progress and remaining scope. They are not validated production forecasts or proof of financial savings.'}
]

class EvidenceAssistant:
    def __init__(self,documents=None):
        self.documents=POLICIES if documents is None else documents
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),stop_words='english')
        self.matrix=self.vectorizer.fit_transform([d['text'] for d in self.documents])

    def ask(self,question,limit=2):
        score=cosine_similarity(self.vectorizer.transform([question]),self.matrix)[0]
        ranked=score.argsort()[::-1]
        hits=[{'source':self.documents[i]['id'],'quote':self.documents[i]['text'],'score':float(score[i])}
              for i in ranked[:limit] if score[i]>=.12]
        return {'mode':'extractive_retrieval','abstained':not bool(hits),'evidence':hits,
            'answer':'No supporting evidence found.' if not hits else ' '.join(h['quote'] for h in hits),
            'notice':'Fictional portfolio policies. No legal advice, automated approval or live ERP access.'}

def evaluate_retrieval():
    examples=[('Who can approve a purchase order?','CTRL-01'),
        ('What happens to invoice payment when matching fails?','CTRL-02'),
        ('What evidence is required for variation approval?','CTRL-03'),
        ('What are UAT exit criteria?','CTRL-04'),
        ('What should a buyer do with supplier delivery risk scores?','CTRL-05'),
        ('Are synthetic cost forecasts validated savings?','CTRL-06'),
        ('Write a poem about galaxies',None)]
    assistant=EvidenceAssistant(); rows=[]
    for question,expected in examples:
        result=assistant.ask(question)
        passed=result['abstained'] if expected is None else expected in [r['source'] for r in result['evidence']]
        rows.append({'question':question,'expected':expected,'passed':passed,'result':result})
    return {'test_set':'Small authored smoke set; not an independent NLP benchmark.',
        'passed':sum(r['passed'] for r in rows),'total':len(rows),'cases':rows}

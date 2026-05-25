import os
import psycopg2

def get_conn():
    return psycopg2.connect(
        os.environ["postgresql://ai_interview_copilot_user:yG2DCDf4tHBc1Pn63iYRTixHEucEzxjW@dpg-d8accqlckfvc739coj20-a.frankfurt-postgres.render.com/ai_interview_copilot"]
    )
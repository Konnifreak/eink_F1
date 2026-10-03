from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import json

from .f1Getter.f1Api import F1getter
from .html_output.race_info import generate_session_results_html

app = FastAPI()
f1_api = F1getter()

def get_next_race_and_session_results(f1_api, session_name: str = "Race"):
        next_race = f1_api.get_next_race()
        if next_race:
            print(next_race)
            meeting_key = next_race.get("meeting_key")
            session = f1_api.get_session_by_name(session_name, meeting_key)
            if session:
                print(session)
                session_key = session.get("session_key")
                results = f1_api.get_session_results(session_key, meeting_key)
                if results:
                    output = {
                        "race_info": next_race,
                        "session_info": session,
                        "results": results
                    }
                    return output
                else:
                    print("No results found for the session.")

                return results
        
        else:
            print("No upcoming races found.")

def get_next_race_and_next_session(f1_api):
    next_race = f1_api.get_next_race()
    if next_race:
        print(next_race)
        meeting_key = next_race.get("meeting_key")
        next_session = f1_api.get_next_session(meeting_key)
        output = []
        if next_session:
            print(next_session)
            output.append({
                "race_info": next_race,
                "session_info": next_session,
            })

            return output

        else:
            print("No upcoming sessions found for the race.")
    else:
        print("No upcoming races found.")


@app.get("/next_session")
def next_session():
    
    try:
        return get_next_race_and_next_session(f1_api)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data not found")

@app.get("/session_results")
def session_results(session_name: str = "Race"):
    try:
        return get_next_race_and_session_results(f1_api, session_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data not found")

@app.get("/html/next_session", response_class=HTMLResponse)
def html_next_session():
    try:
        data = next_session()
        html_content = f"""
        <html>
            <head>
                <title>Next Race and Session</title>
            </head>
            <body>
                <h1>Next Race and Session</h1>
                <pre>{json.dumps(data, indent=4)}</pre>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data not found")

@app.get("/html/session_results", response_class=HTMLResponse)
def html_session_results(session_name: str = "Race"):
    try:
        data = session_results(session_name)
        html_content = generate_session_results_html(data)
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data not found")
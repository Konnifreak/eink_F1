from .f1Getter.f1Api import F1getter
import json

def main() -> None:
    

    def get_next_race_and_session_results(f1_api):
        next_race = f1_api.get_next_race()
        if next_race:
            print(next_race)
            meeting_key = next_race.get("meeting_key")
            session_name = "Race"
            session = f1_api.get_session_by_name(session_name, meeting_key)
            if session:
                print(session)
                session_key = session.get("session_key")
                results = f1_api.get_session_results(session_key, meeting_key)
                if results:
                    print(results)
                else:
                    print("No results found for the session.")

                with open("qualifying_results.json", "w") as f:
                    json.dump(results, f)
        
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

                with open("next_race_and_session.json", "w") as f:
                    json.dump(output, f)
            else:
                print("No upcoming sessions found for the race.")
        else:
            print("No upcoming races found.")

    f1_api = F1getter()
    print("Fetching next race and session information...")
    get_next_race_and_session_results(f1_api)
    get_next_race_and_next_session(f1_api)

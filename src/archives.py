from tinydb import TinyDB, Query
import datetime

class Archives:
    def __init__(self, db_path="archives.json"):
        self.db = TinyDB(db_path)
        self.targets = self.db.table('targets')

    def save_target(self, profile):
        Target = Query()
        name = profile.get("full_name", "UNKNOWN")
        
        profile["last_updated"] = str(datetime.datetime.now())
        
        self.targets.upsert(profile, Target.full_name == name)
        return f"Target '{name}' archived successfully."

    def load_target(self, name):
        Target = Query()
        result = self.targets.search(Target.full_name == name)
        if result:
            return result[0]
        return None

    def list_targets(self):
        return [t.get("full_name") for t in self.targets.all()]


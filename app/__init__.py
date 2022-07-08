import os
print("Setting Google Auth Environment variables")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./modules/keys/k8s_owner_key.json"

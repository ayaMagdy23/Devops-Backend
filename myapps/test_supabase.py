from supabase import create_client, Client

# Replace these with your actual Supabase credentials
supabase_url = "https://xivukiickdgkworwjums.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhpdnVraWlja2Rna3dvcndqdW1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMxOTM2MjIsImV4cCI6MjA1ODc2OTYyMn0.flnVDYNOYkz67aVRxuR-rw_Tcgb1BmduuEoeZ1fZTCE"

supabase = create_client(supabase_url, supabase_key)
print("Connected to Supabase successfully!")

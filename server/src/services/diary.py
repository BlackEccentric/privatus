# Imports
import datetime

# Main
def createEntry(params, server):
  # Filter message param
  if not 'title' in params or not 'content' in params:
    return "Invalid entry format."

  if type(params['title']) != str or type(params['content']) != str:
    return "Invalid types"
                
  # Create the entry
  print("gate 1")
  create_entry(server, server.user, params['title'], params['content'])
  return "Entry created successfully"

def getEntries(params, server):
  print("Fetching user entries...")
  return get_entries(server, server.user)

def searchEntries(params, server):
  if not 'searchterm' in params:
    return "No search term given."
                
  return search_entries(server, params['searchterm'], server.user)

def deleteEntry(params, server):
  # Check if id is given
  if not 'id' in params:
     return "Id not given"
                
  destroyEntry(server, params['id'], server.user)
  return "Successfuly destroyed entry"

def showEntry(params, server):
  # Check if id is given
  if not 'id' in params:
    return "Id not given"
  
  return get_entry(server, params['id'], server.user)

def editEntry(params, server):
  if not 'id' in params or not 'title' in params or not 'content' in params:
    return "Required parameter not given"
                
  return edit_entry(server, params['id'], server.user, params['title'], params['content'])

# Database handler
def create_entry(server, user, title, body):
  database = server.database
  
  # Check if user is an existing user
  if database.get_user("users", user) == None: # If user does not exist
    return 0
        
  # Insert the entry
  command = f'''INSERT INTO entry (ID, OWNER, TITLE, BODY, DATETIME) VALUES (?, ?, ? , ?, ?);'''
        
  # Get the datetime
  dt = datetime.datetime.now()
        
  # This is going to remove the milliseconds
  time = dt.replace(microsecond=0)
        
  # Get id
  print(str(database) + "gate 2")
  id = get_user_total_entries(database, user) + 1
        
  print(str(database) + "gate 3")
  database.execute(command, (id, user, title, body, time)) # Execute
        
  return "Success"

def edit_entry(server, id, user, title, body):
  '''
  Makes changes to entry with specified id with the given parameters
  '''
  database = server.database
  
  # Get rows
  rows = database.cursor.execute(f"SELECT * FROM entry")

  for row in rows:
            
    if row[0] == id and row[1] == user:
      database.execute(f'UPDATE entry SET ID = ?, OWNER = ?, TITLE = ?, BODY = ?, DATETIME = ? WHERE ID = {id}', (id, user, title, body, row[4]))
        
  return f"Edited entry id {id}"

def search_entries(server, searchterm, user):
  '''
  Return a list of entries with the search term in it's title
  '''
        
  rows = server.database.database.execute("SELECT * FROM entry")
  return_results = []
        
  for row in rows:
    title = row[2].lower()
            
    if searchterm in title and row[1] == user:
      return_results.append(row)
                
  return return_results

def get_entries(server, username):
  '''
  Gets the entries that the user created.
  '''
  rows = server.database.database.execute(f"SELECT * FROM entry")
  return_results = []
        
  for row in rows:
    if row[1] == username:
      return_results.append(row)
                
  return return_results

def get_entry(server, id, user):
  '''
  Gets the entry with the id provided.
  '''
  rows = server.database.database.execute(f"SELECT * FROM entry")
        
  for row in rows:
    if row[1] == user and row[0] == id:
      return row
            
  return None  

def destroyEntry(server, id, user):
  '''
  Destroys the entries with the given id
  '''
    
  server.database.database.execute(f"DELETE from entry WHERE ID={id}")
        
  # Update entries above the current id
  rows = server.database.database.execute(f"SELECT * FROM entry")

  for row in rows:
            
    if row[0] > id and row[1] == user:
      rowid = row[0]
      server.database.database.execute(f'UPDATE entry SET ID = ?, OWNER = ?, TITLE = ?, BODY = ?, DATETIME = ? WHERE ID = {rowid}', (rowid - 1, row[1], row[2], row[3], row[4]))
        
  server.database.database.commit()
  return "Successful"

def get_user_total_entries(database, username):
    '''
    Gets the total entries that the user has
    '''
    
    rows = database.database.execute(f"SELECT * FROM entry")
    results = 0
        
    for row in rows:
      if row[1] == username:
        results += 1
                
    return results

# Message handler
directors = [
  ('createEntry', createEntry),
  ('getEntries', getEntries),
  ('searchEntries', searchEntries),
  ('deleteEntry', deleteEntry),
  ('showEntry', showEntry),
  ('editEntry', editEntry)
]
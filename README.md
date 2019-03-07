# vanlevysite
RPG resources and a SW dice roller app

Overview:
  This is a website to warehouse links to RPG resources, our own RPG resources, and to be a dice roller for games with specialized dice.

Organization:

main project: vanlevysite
  Contains settings, requirements, urls

app 1: vanlevy
  contains things never behind the login middleware; basic info pages for the site

app 2: accounts
  handles all login / logout / register / avatar / etc functions.  Incl. the middleware for the login-protected areas
  user model: username and email required, both must be unique
  user profile: first name, last name, bio, picture
  avatar model: linked to user; name, description, picture

app 3: swdice
  first dice roller app - template for others
  
  hub page: "DockingBay" 
    features:
      gives user a list of rooms they been in (in order of date of first entry)
      form to allow users to enter a new room
      link to page to create a new room
    possible location for messaging (if that gets implemented)
  
  dice roller room:
    dice selector section
    three auto-reloading section: destiny, actions, chat
    
style:
  buttons used as links should include either a preceeding '& # 12298' ( &#12298 ) or trailing '& # 12299' ( &#12299 )

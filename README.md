# Compeer API

A simple API to vote on paired items in a list

## Usage

### Register a user

URL: `/auth/register`  
DATA:  
`username` - Username of the person to register  
`email` - Email of the person to register  
`password` - Raw password of the user (will be sent over SSL in the final so its
secure enough.

RESPONSE:
`200 - OK` with no body if the user was made  
`400 - Bad Request` if the username is taken, or you are missing any fields.
The body will contain a dictionary of all your goofs so you should be ok to show
the user them.

### Get a token for a registered user

URL: `/auth/get-token`  
DATA:  
`username` - Username of the person to log in.  
`password` - Raw password of the person to log in.

RESPONSE:  
`200 - OK` with a body containing a dictionary with one parameter, `token`, which is a string.  
`400 - Bad Request` for wrong username / password. Also returns a dict of all the errors.

NOTES:  
Tokens do not expire, you could log in once and then forever authenticate.

### Hello World

URL: `/hello-world`  
DATA:  
Optional token header to make an authenticated request.

RESPONSE:  
Plain text, `Hello world` if you are anonymous (no token / un recognised) and 
`Hello <username>` if you have the token (the tests fail for this... unverified).

#### References
How to authenticate: http://www.django-rest-framework.org/api-guide/authentication/  
Content Headers: http://www.django-rest-framework.org/api-guide/content-negotiation/


## User stories to implement

#### Key for status column
Symbol	| Meaning
------- | -------
CMP		| Complete
OPN		| Unnasigned
ASN		| Assigned but not started
WRK		| Currently working
-		| No back end code required

### Iteration 1
Status	| Resource	| Ref     | As a  | I want to         | So I can
------- | ---------	| ------- | ----- | ----------------- | ---------------------------------
CMP		| Jacob		| CS105   | User  | log in            | access restricted features
CMP		| Jacob		| CS106   | User  | register          | So I can have an account to log in with
-		| Jacob		| CS116   | User  | log out           | use the app anonymously

### Iteration 2
Status	| Resource	| Ref     | As a  | I want to         | So I can
------- | ---------	| ------- | ----- | ----------------- | ---------------------------------
ASN		| Lee		| CS104   | User  | search for a list | find the list I want
OPN		| 			| CS110   | User  | select the list I would like to vote on | vote on things I care about
ASN		| Jacob		| CS101   | User  | create a list     | add items to vote

### Iteration 3
Done?	| Resource	| Ref     | As a  | I want to         | So I can
------- | ---------	| ------- | ----- | ----------------- | ---------------------------------
OPN		| 			| CS107   | User  | vote on items/lists | engage in community voting
OPN		| 			| CS109   | User  | view a list's items sorted by rank/score | see the best/worst items on the list
OPN		| 			| CS301   | LM    | view lists of which I am a LM | manage my lists

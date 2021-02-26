## Endpoints

All of the endpoints will start with `/api/` to prevent conflicts with routing on the frontend. Additionally, for retrieving data from the API, a JWT(JSON Web Token) needs to be placed in the header of the request.

The fields in the body of the JWT are as follows:

- `public_id` - The public id of the user making the request
- `exp` - The expiry date of the token, by default the duration is 24 hours
- `admin` - Determines if the user is an admin or not to restrict access to routes

## GET

Data can be retrieved by all users from the following endpoints(ideally):

`/menuitems` - Retrieves all menuitems

Data can only be requested from the following endpoints by admins(ideally)  
`/users` - Retrieves all user data  
`/ingredients` - Retrieves all ingredients  
`/orders` - Retrieves all orders

## POST

`/auth/login` - Generates the JWT token and logs a user in  
`/auth/signup` - Creates a user in the system

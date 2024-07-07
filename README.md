# User_Auth_Organization
### Summary of the Task

The task involves creating a user authentication and organization management system using Flask, SQLAlchemy, and Flask-WTF. The system should allow users to register, login, and manage their organizations. The application connects to a PostgreSQL database and provides endpoints for user registration, login, and organization management. Unit tests and end-to-end tests are required to ensure the functionality of the application.

### Program Features

1. **Database Connection**:
   - The application connects to a PostgreSQL database using SQLAlchemy.

2. **User Model**:
   - The `User` model includes fields for `userId`, `firstName`, `lastName`, `email`, `password`, and `phone`.
   - Unique constraints are enforced on `userId` and `email`.

3. **Organization Model**:
   - The `Organization` model includes fields for `orgId`, `name`, and `description`.
   - Each user can belong to multiple organizations, and each organization can have multiple users.

4. **User Registration**:
   - Endpoint: `POST /auth/register`
   - Users can register by providing their `firstName`, `lastName`, `email`, `password`, and `phone`.
   - Upon registration, a default organization is created for the user.
   - The password is hashed before being stored in the database.

5. **User Login**:
   - Endpoint: `POST /auth/login`
   - Users can log in by providing their `email` and `password`.
   - A JWT token is generated upon successful login.

6. **User Details**:
   - Endpoint: `GET /api/users/:id`
   - Logged-in users can access their own details or details of users in organizations they belong to.

7. **Organization Management**:
   - Endpoint: `GET /api/organisations`
   - Logged-in users can retrieve all organizations they belong to or created.
   - Endpoint: `GET /api/organisations/:orgId`
   - Retrieve details of a specific organization.
   - Endpoint: `POST /api/organisations`
   - Create a new organization.

8. **Users in Organization**:
   - Endpoint: `POST /api/organisations/:orgId/users`
   - Add a user to a specific organization.

### Issues Encountered

- **CSRF Token Missing Error**:
  - CSRF tokens were not properly handled, leading to missing CSRF token errors.
  - Attempts to disable CSRF tokens for specific methods and manually adding the token in the payload were unsuccessful.

- **Internal Server Error**:
  - Encountered internal server errors during endpoint testing.

### Deployment

The application was deployed on PythonAnywhere and can be accessed at [User Auth Organization](https://reamageorge.pythonanywhere.com/%20User_Auth_Organization). However, the deployment failed due to the issues mentioned above.


### Requirements
These are listed in requirements.txt

### How to Use the Program
1. Setup**: Ensure you have Python and PostgreSQL installed.
2. Environment Configuration**: with .env file
3. Database Setup
4. Running the Application**
5. Endpoints:
   - **User Registration**: `POST /auth/register`
   - **User Login**: `POST /auth/login`
   - **Get User Details**: `GET /api/users/:id`
   - **Get All Organizations**: `GET /api/organisations`
   - **Get Organization Details**: `GET /api/organisations/:orgId`
   - **Create Organization**: `POST /api/organisations`
   - **Add User to Organization**: `POST /api/organisations/:orgId/users`
6. Testing:
   - Unit tests and end-to-end tests should be placed in the `tests` directory.
   - Run the tests using your preferred testing framework.

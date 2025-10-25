# Command List

## General Commands

**flask init**
- Creates and initializes the database

**flask list**
- Lists all entries for every table
- Desirable: Each table has at least one entry

## User Commands

**flask user create**
- Creates user
- Prompts: Username, Password

**flask user list**
- Lists all users
- Prompts: Format (string/json)
- Desirable: At least one user exists

## Employer Commands

**flask employer create**
- Creates employer
- Prompts: Username, Password, Company Name

**flask employer list**
- Lists all employers
- Desirable: At least one employer exists

**flask employer view-positions**
- View positions created by a specified employer
- Prompts: EmployerID
- Desirable: At least one employer who has created at least one position already exists

**flask employer view-position-shortlist**
- View shortlisted students for a position
- Prompts: EmployerID, PositionID
- Desirable: At least one position with shortlisted students exists

**flask employer create-position**
- Creates internship position
- Prompts: EmployerID, Title, Department, Description
- Desirable: At least one employer exists

**flask employer accept-reject**
- Accept or reject student application
- Prompts: EmployerID, PositionID, StudentID, Status, Message
- Desirable: At least one student shortlisted for a position exists

## Staff Commands

**flask staff create**
- Creates staff
- Prompts: EmployerID, Username, Password
- Desirable: The employer that staff is to be assigned to exists

**flask staff list**
- Lists all staff
- Desirable: At least one staff member exists

**flask staff add-to-shortlist**
- Adds a student to a shortlist
- Prompts: StaffID, PositionID, StudentID
- Desirable: At least one student who does not belong to the target shortlist exists

**flask staff remove-from-shortlist**
- Removes a student from a shortlist
- Prompts: StaffID, PositionID, StudentID
- Desirable: At least one student shortlisted for a position exists

## Student Commands

**flask student create**
- Creates student
- Prompts: Username, Password, Faculty, Department, Degree, GPA

**flask student list**
- Lists all students
- Desirable: At least one student exists

**flask student view-shortlists**
- Lists positions student has been shortlisted for
- Prompts: StudentID
- Desirable: At least one student who has been shortlisted exists

**flask student browse-positions**
- Browse all available positions
- Desirable: At least one position exists

## Position Commands

**flask position list**
- Lists all positions
- Desirable: At least one position exists

**flask position view**
- View details of a specific position
- Prompts: PositionID
- Desirable: At least one position exists

**flask position delete**
- Delete a position
- Prompts: PositionID
- Desirable: At least one position exists

## Test Commands

**flask test user**
- Run User unit tests

**flask test emp**
- Run Employer unit tests

**flask test sta**
- Run Staff unit tests

**flask test std**
- Run Student unit tests
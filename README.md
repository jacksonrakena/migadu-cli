# Migadu CLI

Command line tool for managing Migadu email hosting.

## Examples

#### Setup
Add your [Migadu API key](https://admin.migadu.com/account/api/keys):
```sh
mictl setup my-admin-email@example.com SDUMz11DCEyJJOIvmODI8bJ7HwfJkDFVJif9Ds9df38VDj83xG3sJOVIjfmSdofvndZjIJfoivnODIfn
```

### Creation
To create a mailbox with a password:
```
mictl boxes create test@example.com --name "Test User" --password helloworld
```

To create a mailbox with a random password:
```
mictl boxes create test@example.com --name "Test User" --random
```

To create a mailbox and send a password reset email to an address:
```
mictl boxes create test@example.com --name "Test User" --invite-address otheraddress@example.com
```

### Deletion
Delete a mailbox:
```
mictl boxes delete test@example.com
```

## Copyright
Mictl copyright &copy; 2019-2022 Jackson C. Rakena  
All properties copyright of their respective authors.

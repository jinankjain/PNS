## Design Documentation for API provided by Maintainer

This section will contain all the documentation related to APIs provided by maintainer which people would query to get information about page

### Set of Public APIs
These APIs are bascialy for the client who is trying to fetch a page from the maintainer.

- API for getting current page with page\_id 'id'

```
/get_page/page_id=id
```
- API for getting differential update for page with page\_id 'id' and current\_version field is to indicate the current version of the client who is asking for the page. 

```
/get_page/page_id=id&current_version=ver
```

### Set of Private APIs
These APIs are bascially for the maintainer to update pages and information related to the maintainer

- API for updating pages entry

```
/update_page/page_id=id&entry=SHA256&ARecord=[]
```


Curve25519
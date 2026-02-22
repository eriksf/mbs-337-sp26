Introduction to APIs
=====================

In this section, we will discuss Application Programming Interfaces (APIs)
focusing on Web APIs, and in particular REST APIs. We will learn how to interact
with APIs using Python scripts. After going through this module, students should
be able to:

* Identify and describe Web APIs (including REST APIs).
* List the four most important HTTP verbs and define how they are used in REST APIs.
* Describe how URLs are used to represent objects in a REST API.
* Explore API endpoints provided by various websites, e.g., GitHub.
* Install the Python ``requests`` library, and use it to interact with a web API
  in a Python script, including making requests and parsing responses.
* **Design Principles**: Additionally, we will see how designing software with APIs
  contributes to the *modularity*, *portability*, *abstraction* and *generalization*
  of software (all four major design principles).


What are APIs?
--------------

An Application Programming Interface (API) establishes the protocols and methods
for one piece of a program to communicate with another. APIs are useful for
allowing large software systems to be built from smaller components, allowing the
same components to be used by different systems, and insulating consumers from
changes to the implementation.

Some examples of where you might see APIs implemented:

* In OOP languages, abstract classes provide the interface for all concrete
  classes to implement.
* Software libraries provide an external interface for consuming programs.
* Web APIs (or “web services”) provide interfaces for computer programs to
  communicate over the internet.

While a User Interface connects humans to computer programs, an API is an interface
that connects one piece of software to another. Specifically, APIs:

* Provide functionality to external software in the form of a contract that specifies
  the inputs that the consuming software must provide and the outputs that the API
  will produce from the inputs.
* Conceal the implementation of this functionality from the consuming software so
  that changes can be made to the implementation without impacting consumers.
* Provide errors when the consuming software doesn't fulfill the contract of the API or when
  unexpected circumstances are encountered.

We have already been working with APIs. For example, the Python ``json`` library
presents us with an API for working with JSON data. Try opening up the Python3
interactive interpreter:

.. code-block:: console

   [mbs337-vm]$ cd $HOME/mbs-337
   [mbs337-vm]$ source .venv/bin/activate
   [mbs337-vm]$ python3
   Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

And enter the following:

.. code-block:: python3

   >>> import json
   >>> dir(json)
   ['JSONDecodeError', 'JSONDecoder', ... 'dump', 'dumps', 'encoder', 'load', 'loads', 'scanner']

We use ``json.dumps()`` to convert Python objects to JSON (string) data and we use
``json.loads()`` to convert JSON strings to Python objects.

.. code-block:: python3

    >>> json.dumps({'a': 1})
    '{"a": 1}'
    >>> type(_)
    <class 'str'>
    >>> json.loads('{"a": 1}')
    {'a': 1}
    >>> type(_)
    <class 'dict'>

We say that ``dumps`` and ``loads`` are part of the Python ``json`` API. In terms of the
contract, we might say something like:

* ``json.loads()`` -- This function accepts a single input (string, bytes or bytes array) representing
  a valid JSON document and returns the equivalent Python object.

  * It will raise a ``JSONDecodeError`` if the input is not a valid JSON document.

* ``json.dumps()`` -- This function accepts a single input (a Python object) and serializes
  it to a string. The Python object must be JSON serializable.

  * It will raise a ``TypeError`` if the input is not JSON serializable.


**Design Principles.** Can you see how the existence of the API provided by the ``json`` module increases modularity of the Python
software ecosystem?


Web APIs / HTTP
---------------

In this course, we will be looking at Web APIs or HTTP APIs. These are interfaces
that are exposed over HTTP, allowing them to be consumed by software running on different
machines.

There are a number of advantages to Web-based APIs that we will use in this class:

* A Web API can be made accessible to any computer or application that can access
  the public internet. Alternatively, a Web API can be restricted to a private network.
* No software installation is required on the client's side to consume a Web API.
* Web APIs can change their implementation without clients knowing (or caring).
* Virtually every modern programming language provides one or more libraries for
  interacting with a Web API; thus, Web APIs are "programming language agnostic".


HTTP (Hyper Text Transfer Protocol) is one way for two computers on the internet
to communicate with each other. It was designed to enable the exchange of data
(specifically, "hypertext"). In particular, our web browsers use HTTP when
communicating with web servers running web applications. HTTP uses a
message-based, **client-server model**: clients make requests to servers by
sending a message, and servers respond by sending a message back to the client.

HTTP is an "application layer" protocol in the language of the
Internet Protocols; it assumes a lower level transport layer protocol. While
this can swapped, in practice it is almost always TCP (Transmission Control Protocol). The basics of the
protocol are:

* Web resources are identified with URLs (Uniform Resource Locators).
  Originally, **resources** were just files/directories on a server, but today
  resources refer to more general objects.
* HTTP **verbs** represent actions to take on the resource. The most common verbs
  are ``GET``, ``POST``, ``PUT``, and ``DELETE``.
* A **request** is made up of a URL, an HTTP verb, and a message
* A **response** consists of a status code (numerical between 100-599) and a
  message. The first digit of the status code specifies the kind of response:

    * 1xx - informational
    * 2xx - success
    * 3xx - redirection
    * 4xx - error in the request (client)
    * 5xx - error fulfilling a valid request (server)


Web Page Examples
-----------------

Open a browser window, type ``https://github.com`` into the address bar and hit go.
We see the GitHub home page which looks something like this:


.. figure:: images/github-home.png
    :width: 600px
    :align: center


In fact, a multi-step process just occurred; here is a slightly simplified version of what
happened:

(1) Your browser made an HTTP GET request to https://github.com.
(2) A GitHub server received the request from your browser, formulated a response message
    containing the data (in HTML format) of your home page, with a 200 response code
    to indicate success.
(3) Your browser received the response message from the GitHub server, and determined that
    the request was successful, due to the 200 response code.
(4) It then drew the HTML message in the browser window.

If we enter a URL that GitHub doesn't recognize, we get a page that looks like this:

.. figure:: images/github-404.png
    :width: 600px
    :align: center

Most browsers have tools for determining what requests and responses were made. For example,
in Chrome, we can use "More Tools -> Developer Tools" from the Customize and Control menu
(the three dots in the top-right corner), to open up a panel for introspecting the requests
being made.

If we click the "Network" tab and try our request again, we will see something like this:

.. figure:: images/github-404-network.png
    :width: 600px
    :align: center

The top row in red represents the request to ``https://github.com/aqw1Z9463`` and it shows
the status code of the response was 404.


REST APIs - Overview
--------------------

REST (Representational State Transfer) is a way of building APIs for computer
programs on the internet leveraging HTTP. In other words, a program on computer
1 interacts with a program on computer 2 by making an HTTP request to it and receiving HTTP
responses.

The basic idea with REST is to associate objects in the application domain with URLs,
and to use HTTP verbs to represent the actions we want to take on the objects.
A REST API has a **base URL** from which all other URLs in
that API are formed. For example, the base URL for the GitHub REST API which we will look
at in more detail momentarily is ``https://api.github.com/``.


The other URLs in the API are then "collections", typically represented by a plural noun,
following the base URL; e.g.:

.. code-block:: console

   <base_url>/users
   <base_url>/files
   <base_url>/programs

Or they are specific items in a collection, represented by an identifier following the
collection name, e.g.:

.. code-block:: console

   <base_url>/users/12345
   <base_url>/files/test.txt
   <base_url>/programs/myapplication


Or subcollections or items in subcollections, e.g.:

.. code-block:: console

   <base_url>/companies/<company_id>/employees
   <base_url>/companies/<company_id>/employees/<employee_id>


As mentioned, the HTTP verbs represent “operations” or actions that can be taken
on the resources:

* ``GET`` - list items in a collection or retrieve a specific item in the
  collection
* ``POST`` - create a new item in the collection based on the description in the
  message
* ``PUT`` - replace an item in a collection with the description in the message
* ``DELETE`` - delete an item in a collection

Thus,

* ``GET <base_url>/users``  would list all users.
* ``POST <base_url>/users`` would create a new user.
* ``PUT <base_url>/users/12345`` would update user 12345.
* ``DELETE <base_url>/users/98765`` would delete user 98765.

The combination of an HTTP verb and URL (path) is called an **endpoint** in an API. A REST
API is typically comprised of many endpoints. Note that not all HTTP verbs make sense for all URLs.
For example, an API would probably not include a PUT ``<base_url>/users`` endpoint, because
semantically, that would mean updating the entire list of users.

.. note::

   Response messages often make use of some data serialization format standard such
   as JSON, CSV or XML.

**Design Principles.** Note that the architecture of REST, combining URL paths that represent *resources* with
HTTP verbs that represnt *actions* to take on resources, constitutes *abstraction* and *generalization* as a large
number of applications can be described in this way.


REST APIs - Additional Simple Examples
--------------------------------------

Virtually every application domain can be mapped into a REST API architecture.
Some examples may include:

Articles in a collection (e.g., on a blog or wiki) with author attributes:

.. code-block:: console

   <base_url>/articles
   <base_url>/articles/<id>
   <base_url>/articles/<id>/authors


Properties in a real estate database with associated purchase history:

.. code-block:: console

   <base_url>/properties
   <base_url>/properties/<id>
   <base_url>/properties/<id>/purchases


A catalog of countries, cities and neighborhoods:

.. code-block:: console

   <base_url>/countries
   <base_url>/countries/<country_id>/cities
   <base_url>/countries/<country_id>/cities/<city_id>/neighborhoods


REST APIs - A Real Example
--------------------------

We have been using GitHub to host our class code repositories. It turns out GitHub
provides an HTTP API that is architected using REST (for the most part). We're going
to explore the GitHub API.

To begin, open a web browser and navigate to https://api.github.com

You will see something like this:

.. code-block:: console

  {
    "current_user_url": "https://api.github.com/user",
    "current_user_authorizations_html_url": "https://github.com/settings/connections/applications{/client_id}",
    "authorizations_url": "https://api.github.com/authorizations",
    "code_search_url": "https://api.github.com/search/code?q={query}{&page,per_page,sort,order}",
    "commit_search_url": "https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}",
    "emails_url": "https://api.github.com/user/emails",
    "emojis_url": "https://api.github.com/emojis",
    "events_url": "https://api.github.com/events",
    "feeds_url": "https://api.github.com/feeds",
    "followers_url": "https://api.github.com/user/followers",
    "following_url": "https://api.github.com/user/following{/target}",
    "gists_url": "https://api.github.com/gists{/gist_id}",
    "hub_url": "https://api.github.com/hub",
    "issue_search_url": "https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}",
    "issues_url": "https://api.github.com/issues",
    "keys_url": "https://api.github.com/user/keys",
    "label_search_url": "https://api.github.com/search/labels?q={query}&repository_id={repository_id}{&page,per_page}",
    "notifications_url": "https://api.github.com/notifications",
    "organization_url": "https://api.github.com/orgs/{org}",
    "organization_repositories_url": "https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}",
    "organization_teams_url": "https://api.github.com/orgs/{org}/teams",
    "public_gists_url": "https://api.github.com/gists/public",
    "rate_limit_url": "https://api.github.com/rate_limit",
    "repository_url": "https://api.github.com/repos/{owner}/{repo}",
    "repository_search_url": "https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}",
    "current_user_repositories_url": "https://api.github.com/user/repos{?type,page,per_page,sort}",
    "starred_url": "https://api.github.com/user/starred{/owner}{/repo}",
    "starred_gists_url": "https://api.github.com/gists/starred",
    "topic_search_url": "https://api.github.com/search/topics?q={query}{&page,per_page}",
    "user_url": "https://api.github.com/users/{user}",
    "user_organizations_url": "https://api.github.com/user/orgs",
    "user_repositories_url": "https://api.github.com/users/{user}/repos{?type,page,per_page,sort}",
    "user_search_url": "https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"
  }

This should look familiar -- it's a JSON document, and it describes various collections of
endpoints in the GitHub API. For example, we see:

* ``"events_url": "https://api.github.com/events",`` -- Work with GitHub events
* ``"organization_url": "https://api.github.com/orgs/{org}",`` -- Work with GitHub orgs
* ``"repository_url": "https://api.github.com/repos/{owner}/{repo}",`` -- Work with GitHub repos

Many of the endpoints within the GitHub API require *authentication*, i.e., that the requesting
application prove its identity -- we'll ignore this topic for now and just work with the
endpoints that do not require authentication.

Let's discover what the GitHub API can tell us about TACC's GitHub organization, which is
just called ``tacc``.

EXERCISE
~~~~~~~~

Based on the information above, how would we retrieve information about the TACC GitHub
organization from the API? What HTTP verb and URL would we use?

SOLUTION
~~~~~~~~

We see that the "organization_url" is defined to be ``"https://api.github.com/orgs/{org}"``.
The use of the ``{org}`` notation is common in API documentation -- it indicates a variable
to be substituted with a value. In this case, we should substitute ``tacc`` for ``{org}``,
as that is the organization we are interested in.

Since we want to retrieve (or list) information about the TACC organization, the HTTP verb
we want to use is GET.

We can use the browser to make this request, as before. If we enter
``https://api.github.com/orgs/tacc`` into the URL bar, we should see:

.. code-block:: console

  {
    "login": "TACC",
    "id": 840408,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjg0MDQwOA==",
    "url": "https://api.github.com/orgs/TACC",
    "repos_url": "https://api.github.com/orgs/TACC/repos",
    "events_url": "https://api.github.com/orgs/TACC/events",
    "hooks_url": "https://api.github.com/orgs/TACC/hooks",
    "issues_url": "https://api.github.com/orgs/TACC/issues",
    "members_url": "https://api.github.com/orgs/TACC/members{/member}",
    "public_members_url": "https://api.github.com/orgs/TACC/public_members{/member}",
    "avatar_url": "https://avatars.githubusercontent.com/u/840408?v=4",
    "description": "",
    "name": "Texas Advanced Computing Center",
    "company": null,
    "blog": "http://www.tacc.utexas.edu",
    "location": "Austin, TX",
    "email": null,
    "twitter_username": null,
    "is_verified": false,
    "has_organization_projects": true,
    "has_repository_projects": true,
    "public_repos": 225,
    "public_gists": 0,
    "followers": 103,
    "following": 0,
    "html_url": "https://github.com/TACC",
    "created_at": "2011-06-09T16:47:08Z",
    "updated_at": "2022-07-12T16:29:02Z",
    "archived_at": null,
    "type": "Organization"
  }


Using Python to Interact with Web APIs
--------------------------------------

Viewing API response messages in a web browser provides limited utility. We can
interact with Web APIs in a much more powerful and programmatic way using the
Python ``requests`` library.

First install the ``requests`` library in your local site-packages on the ISP server using
pip3:

.. code-block:: console

   [mbs337-vm]$ cd $HOME/mbs-337
   [mbs337-vm]$ source .venv/bin/activate
   (.venv) [mbs337-vm]$ pip3 install requests
   ...
   Successfully installed certifi-2026.1.4 charset_normalizer-3.4.4 idna-3.11 requests-2.32.5 urllib3-2.6.3
   (.venv) [mbs337-vm]$ pip3 list
   Package            Version
   ------------------ --------
   annotated-types    0.7.0
   biopython          1.86
   certifi            2026.1.4
   charset-normalizer 3.4.4
   idna               3.11
   iniconfig          2.3.0
   numpy              2.4.1
   packaging          26.0
   pip                24.0
   pluggy             1.6.0
   pydantic           2.12.5
   pydantic_core      2.41.5
   Pygments           2.19.2
   pytest             9.0.2
   redis              7.2.0
   requests           2.32.5
   typing_extensions  4.15.0
   typing-inspection  0.4.2
   urllib3            2.6.3

You might test that the install was successful by trying to import the library
in the interactive Python interpreter:

.. code-block:: console

   [mbs337-vm]$ python3
   Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import requests
   >>>


The basic usage of the ``requests`` library is as follows:

.. code-block:: python3

   >>> # make a request: typical format
   >>> # response = requests.<method>(url=some_url, data=some_message, <other options>)
   >>>
   >>> # e.g. try:
   >>> response = requests.get(url='https://api.github.com/orgs/tacc')
   >>>
   >>> # return the status code:
   >>> response.status_code
   >>>
   >>> # return the raw content
   >>> response.content
   >>>
   >>> # return a Python list or dictionary from the response message
   >>> response.json()


EXERCISE
~~~~~~~~

Let's use ``requests`` to explore the GitHub API. Write functions to return the following:

* Given a GitHub organization id (``tacc``), retrieve all information about the organization. Return
  the information as a Python dictionary.
* Given a GitHub organization id, retrieve a list of all of the members of the organization.
  Return the list of members as a Python list of strings, where each string contains the member's
  ``login`` (i.e., GitHub username) attribute.
* Given a GitHub organization id, return a list of repositories controlled by the organization.
  Return the list of repositories as a Python list of strings, where each string contains the
  repository ``full_name`` attribute.

.. toggle:: Click

  .. code-block:: console

    >>> r = requests.get(url="https://api.github.com/orgs/tacc")
    >>> r.status_code
    200
    >>> tacc = r.json()
    >>> print(tacc)
    {'login': 'TACC', 'id': 840408, 'node_id': 'MDEyOk9yZ2FuaXphdGlvbjg0MDQwOA==', 'url': 'https://api.github.com/orgs/TACC', 'repos_url': 'https://api.github.com/orgs/TACC/repos', 'events_url': 'https://api.github.com/orgs/TACC/events', 'hooks_url': 'https://api.github.com/orgs/TACC/hooks', 'issues_url': 'https://api.github.com/orgs/TACC/issues', 'members_url': 'https://api.github.com/orgs/TACC/members{/member}', 'public_members_url': 'https://api.github.com/orgs/TACC/public_members{/member}', 'avatar_url': 'https://avatars.githubusercontent.com/u/840408?v=4', 'description': '', 'name': 'Texas Advanced Computing Center', 'company': None, 'blog': 'http://www.tacc.utexas.edu', 'location': 'Austin, TX', 'email': None, 'twitter_username': None, 'is_verified': False, 'has_organization_projects': True, 'has_repository_projects': True, 'public_repos': 225, 'public_gists': 0, 'followers': 103, 'following': 0, 'html_url': 'https://github.com/TACC', 'created_at': '2011-06-09T16:47:08Z', 'updated_at': '2022-07-12T16:29:02Z', 'archived_at': None, 'type': 'Organization'}
    >>> type(tacc)
    <class 'dict'>
    >>>
    >>>
    >>> r = requests.get(url="https://api.github.com/orgs/TACC/members")
    >>> r.status_code
    200
    >>> tacc_members = r.json()
    >>> print(tacc_members[0])
    {'login': 'annedara', 'id': 2905303, 'node_id': 'MDQ6VXNlcjI5MDUzMDM=', 'avatar_url': 'https://avatars.githubusercontent.com/u/2905303?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/annedara', 'html_url': 'https://github.com/annedara', 'followers_url': 'https://api.github.com/users/annedara/followers', 'following_url': 'https://api.github.com/users/annedara/following{/other_user}', 'gists_url': 'https://api.github.com/users/annedara/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/annedara/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/annedara/subscriptions', 'organizations_url': 'https://api.github.com/users/annedara/orgs', 'repos_url': 'https://api.github.com/users/annedara/repos', 'events_url': 'https://api.github.com/users/annedara/events{/privacy}', 'received_events_url': 'https://api.github.com/users/annedara/received_events', 'type': 'User', 'user_view_type': 'public', 'site_admin': False}
    >>> logins = [m['login'] for m in tacc_members]
    >>> print(logins)
    ['annedara', 'GregAbram', 'happycodemonkey', 'jamescarson3', 'mpackard', 'mrcawood', 'nathanfranklin', 'nmendoza', 'NotChristianGarcia', 'pnav', 'rstijerina', 'rtmclay', 'scottre', 'semeraro', 'stephenlienharrell', 'VictorEijkhout', 'wesleyboar', 'wjallen']
    >>> type(logins)
    <class 'list'>
    >>>
    >>>
    >>> r = requests.get(url="https://api.github.com/orgs/TACC/repos")
    >>> r.status_code
    200
    >>> tacc_repos = r.json()
    >>> print(tacc_repos[0])
    {'id': 2217610, 'node_id': 'MDEwOlJlcG9zaXRvcnkyMjE3NjEw', 'name': 'DisplayCluster', 'full_name': 'TACC/DisplayCluster', 'private': False, 'owner': {'login': 'TACC', 'id': 840408, 'node_id': 'MDEyOk9yZ2FuaXphdGlvbjg0MDQwOA==', 'avatar_url': 'https://avatars.githubusercontent.com/u/840408?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/TACC', 'html_url': 'https://github.com/TACC', 'followers_url': 'https://api.github.com/users/TACC/followers', 'following_url': 'https://api.github.com/users/TACC/following{/other_user}', 'gists_url': 'https://api.github.com/users/TACC/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/TACC/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/TACC/subscriptions', 'organizations_url': 'https://api.github.com/users/TACC/orgs', 'repos_url': 'https://api.github.com/users/TACC/repos', 'events_url': 'https://api.github.com/users/TACC/events{/privacy}', 'received_events_url': 'https://api.github.com/users/TACC/received_events', 'type': 'Organization', 'user_view_type': 'public', 'site_admin': False}, 'html_url': 'https://github.com/TACC/DisplayCluster', 'description': 'a collaborative software environment for large-scale tiled display systems', 'fork': False, 'url': 'https://api.github.com/repos/TACC/DisplayCluster', 'forks_url': 'https://api.github.com/repos/TACC/DisplayCluster/forks', 'keys_url': 'https://api.github.com/repos/TACC/DisplayCluster/keys{/key_id}', 'collaborators_url': 'https://api.github.com/repos/TACC/DisplayCluster/collaborators{/collaborator}', 'teams_url': 'https://api.github.com/repos/TACC/DisplayCluster/teams', 'hooks_url': 'https://api.github.com/repos/TACC/DisplayCluster/hooks', 'issue_events_url': 'https://api.github.com/repos/TACC/DisplayCluster/issues/events{/number}', 'events_url': 'https://api.github.com/repos/TACC/DisplayCluster/events', 'assignees_url': 'https://api.github.com/repos/TACC/DisplayCluster/assignees{/user}', 'branches_url': 'https://api.github.com/repos/TACC/DisplayCluster/branches{/branch}', 'tags_url': 'https://api.github.com/repos/TACC/DisplayCluster/tags', 'blobs_url': 'https://api.github.com/repos/TACC/DisplayCluster/git/blobs{/sha}', 'git_tags_url': 'https://api.github.com/repos/TACC/DisplayCluster/git/tags{/sha}', 'git_refs_url': 'https://api.github.com/repos/TACC/DisplayCluster/git/refs{/sha}', 'trees_url': 'https://api.github.com/repos/TACC/DisplayCluster/git/trees{/sha}', 'statuses_url': 'https://api.github.com/repos/TACC/DisplayCluster/statuses/{sha}', 'languages_url': 'https://api.github.com/repos/TACC/DisplayCluster/languages', 'stargazers_url': 'https://api.github.com/repos/TACC/DisplayCluster/stargazers', 'contributors_url': 'https://api.github.com/repos/TACC/DisplayCluster/contributors', 'subscribers_url': 'https://api.github.com/repos/TACC/DisplayCluster/subscribers', 'subscription_url': 'https://api.github.com/repos/TACC/DisplayCluster/subscription', 'commits_url': 'https://api.github.com/repos/TACC/DisplayCluster/commits{/sha}', 'git_commits_url': 'https://api.github.com/repos/TACC/DisplayCluster/git/commits{/sha}', 'comments_url': 'https://api.github.com/repos/TACC/DisplayCluster/comments{/number}', 'issue_comment_url': 'https://api.github.com/repos/TACC/DisplayCluster/issues/comments{/number}', 'contents_url': 'https://api.github.com/repos/TACC/DisplayCluster/contents/{+path}', 'compare_url': 'https://api.github.com/repos/TACC/DisplayCluster/compare/{base}...{head}', 'merges_url': 'https://api.github.com/repos/TACC/DisplayCluster/merges', 'archive_url': 'https://api.github.com/repos/TACC/DisplayCluster/{archive_format}{/ref}', 'downloads_url': 'https://api.github.com/repos/TACC/DisplayCluster/downloads', 'issues_url': 'https://api.github.com/repos/TACC/DisplayCluster/issues{/number}', 'pulls_url': 'https://api.github.com/repos/TACC/DisplayCluster/pulls{/number}', 'milestones_url': 'https://api.github.com/repos/TACC/DisplayCluster/milestones{/number}', 'notifications_url': 'https://api.github.com/repos/TACC/DisplayCluster/notifications{?since,all,participating}', 'labels_url': 'https://api.github.com/repos/TACC/DisplayCluster/labels{/name}', 'releases_url': 'https://api.github.com/repos/TACC/DisplayCluster/releases{/id}', 'deployments_url': 'https://api.github.com/repos/TACC/DisplayCluster/deployments', 'created_at': '2011-08-16T19:05:01Z', 'updated_at': '2025-01-31T23:40:15Z', 'pushed_at': '2026-01-26T18:32:10Z', 'git_url': 'git://github.com/TACC/DisplayCluster.git', 'ssh_url': 'git@github.com:TACC/DisplayCluster.git', 'clone_url': 'https://github.com/TACC/DisplayCluster.git', 'svn_url': 'https://github.com/TACC/DisplayCluster', 'homepage': '', 'size': 129751, 'stargazers_count': 40, 'watchers_count': 40, 'language': 'C++', 'has_issues': True, 'has_projects': True, 'has_downloads': True, 'has_wiki': False, 'has_pages': False, 'has_discussions': False, 'forks_count': 27, 'mirror_url': None, 'archived': False, 'disabled': False, 'open_issues_count': 17, 'license': {'key': 'other', 'name': 'Other', 'spdx_id': 'NOASSERTION', 'url': None, 'node_id': 'MDc6TGljZW5zZTA='}, 'allow_forking': True, 'is_template': False, 'web_commit_signoff_required': False, 'has_pull_requests': True, 'pull_request_creation_policy': 'all', 'topics': [], 'visibility': 'public', 'forks': 27, 'open_issues': 17, 'watchers': 40, 'default_branch': 'main', 'permissions': {'admin': False, 'maintain': False, 'push': False, 'triage': False, 'pull': True}, 'custom_properties': {}}
    >>> repos = [r['full_name'] for r in tacc_repos]
    >>> print(repos)
    ['TACC/DisplayCluster', 'TACC/pylauncher', 'TACC/laser', 'TACC/latex_templates', 'TACC/MassivePixelEnvironment', 'TACC/t3pio', 'TACC/liferay-scala-portlet', 'TACC/GDBase', 'TACC/filemanager', 'TACC/CLUS', 'TACC/launcher', 'TACC/lariat', 'TACC/Lmod', 'TACC/GLuRay', 'TACC/perfexpert', 'TACC/ShellStartupDebug', 'TACC/Hermes', 'TACC/Themis', 'TACC/HPCPerfStats', 'TACC/vtkOSPRay', 'TACC/GraviT', 'TACC/pvOSPRay', 'TACC/visitOSPRay', 'TACC/SDVis', 'TACC/VolViewer', 'TACC/agavepy', 'TACC/abaco', 'TACC/channelpy', 'TACC/remora', 'TACC/hpc_spec']
    >>> type(repos)
    <class 'list'>
    >>>

**Design Principles.** We will use the concept of web APIs in a critical way for developing portable software. As
web APIs are accessible to any software running in an environment with a stable internet connection, we can build
software components distributed across different computers (and even the entire internet) that work together. The
precise locations of the software components won't matter and, when combined with other techniques, we will be able
to freely move those components around and still have a fully functioning system.

Additional Resources
--------------------

* Many of the materials in this module were adapted from `COE 332: Software Engineering & Design <https://coe-332-sp26.readthedocs.io/en/latest/unit06/intro_to_apis.html>`_

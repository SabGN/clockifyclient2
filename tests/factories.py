""" Shared classes used in other tests. For generating test data """
from itertools import cycle
from typing import List
from unittest.mock import Mock
from requests.models import Response


class RequestMockResponse:
    """A description of a http server response
    """

    def __init__(self, text, response_code):
        """

        Parameters
        ----------
        text: str
            Text of this response
        response_code: int
            https response code, like 200 or 404
        """

        self.text = text
        self.response_code = response_code


class RequestsMock:
    """ Can be put in place of the requests module. Can be set to return requests.models.Response objects

    """

    def __init__(self):
        self.requests = Mock()  # for keeping track of past requests
        self.http_methods = [self.requests.get,
                             self.requests.post,
                             self.requests.patch,
                             self.requests.update]

    def set_response(self, response: RequestMockResponse):
        """Just for convenience"""
        self.set_responses([response])

    def set_responses(self, responses: List[RequestMockResponse]):
        """Any call to a http method will yield the given response. A list of responses will be looped over
        indefinitely

        Parameters
        ----------
        responses: List[RequestMockResponse]
            List of responses. Will be returned
        """

        objects = [
            self.create_response_object(response.response_code, response.text)
            for response in responses
        ]

        for method in self.http_methods:
            method.side_effect = cycle(objects)

    def set_response_exception(self, exception):
        """Any call to a http method will yield the given exception instance
        """
        for method in self.http_methods:
            method.side_effect = exception

    @staticmethod
    def create_response_object(status_code, text):
        response = Response()
        response.encoding = "utf-8"
        response.status_code = status_code
        response._content = bytes(text, response.encoding)
        response.url = "mock_url"
        return response

    def get(self, *args, **kwargs):
        return self.requests.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.requests.post(*args, **kwargs)

    def reset(self):
        self.requests.reset_mock()

    def called(self):
        """True if any http method was called"""
        return any([x.called for x in self.http_methods])


class ClockifyMockResponses:
    """Some cached examples of http responses from Clockify API v1. These partly come from https://clockify.me/developers-api
    and party were recorded by interacting with the server live around november 2019
    """

    # with non-existent API or missing key
    AUTH_ERROR = RequestMockResponse(
        '{"description":"Full authentication is required to access this resource","code":1000}',
        401,
    )

    # Trying to set something on
    CURRENTLY_RUNNING_ENTRY_NOT_FOUND = RequestMockResponse(
        """{"message":"Currently running time entry doesn't exist on workspace 123456 for user 123456.","code":404}""",
        404
    )

    # calling get /workspaces
    GET_WORKSPACES = RequestMockResponse(
        """ [
            {
                "id": "5e5b8b0a95ae537fbde06e2f",
                "name": "Lewis Carroll's workspace",
                "hourlyRate": {
                    "amount": 0,
                    "currency": "USD"
                },
                "memberships": [
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b8b0a95ae537fbde06e2f",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "workspaceSettings": {
                    "timeRoundingInReports": false,
                    "onlyAdminsSeeBillableRates": true,
                    "onlyAdminsCreateProject": true,
                    "onlyAdminsSeeDashboard": false,
                    "defaultBillableProjects": true,
                    "isProjectPublicByDefault": true,
                    "lockTimeEntries": null,
                    "round": {
                        "round": "Round to nearest",
                        "minutes": "15"
                    },
                    "projectFavorites": true,
                    "canSeeTimeSheet": false,
                    "projectPickerSpecialFilter": false,
                    "forceProjects": false,
                    "forceTasks": false,
                    "forceTags": false,
                    "forceDescription": false,
                    "onlyAdminsSeeAllTimeEntries": false,
                    "onlyAdminsSeePublicProjectsEntries": false,
                    "trackTimeDownToSecond": true,
                    "projectGroupingLabel": "client",
                    "adminOnlyPages": [],
                    "automaticLock": null,
                    "onlyAdminsCreateTag": false
                },
                "imageUrl": "",
                "featureSubscriptionType": null
            },
            {
                "id": "5e5b8b3a95ae537fbde06e58",
                "name": "Alice in Wonderland",
                "hourlyRate": {
                    "amount": 10000,
                    "currency": "GBP"
                },
                "memberships": [
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b91837df81c0df5f29609",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b94837df81c0df5f2979c",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b998195ae537fbde0761d",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "workspaceSettings": {
                    "timeRoundingInReports": false,
                    "onlyAdminsSeeBillableRates": true,
                    "onlyAdminsCreateProject": true,
                    "onlyAdminsSeeDashboard": false,
                    "defaultBillableProjects": true,
                    "isProjectPublicByDefault": true,
                    "lockTimeEntries": null,
                    "round": {
                        "round": "Round to nearest",
                        "minutes": "15"
                    },
                    "projectFavorites": true,
                    "canSeeTimeSheet": false,
                    "projectPickerSpecialFilter": false,
                    "forceProjects": false,
                    "forceTasks": false,
                    "forceTags": false,
                    "forceDescription": false,
                    "onlyAdminsSeeAllTimeEntries": false,
                    "onlyAdminsSeePublicProjectsEntries": false,
                    "trackTimeDownToSecond": false,
                    "projectGroupingLabel": "client",
                    "adminOnlyPages": [],
                    "automaticLock": null,
                    "onlyAdminsCreateTag": false
                },
                "imageUrl": "https://img.clockify.me/2020-03-01T11%3A07%3A16.041ZIn+Wonderland.jpg",
                "featureSubscriptionType": null
            }
        ] """,
        200
    )

    # calling get /user
    GET_USER = RequestMockResponse(
        """
            {
                "id": "5e5b8b0a95ae537fbde06e2e",
                "email": "lewis_carroll_1832@mail.ru",
                "name": "Lewis Carroll",
                "memberships": [
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b8b0a95ae537fbde06e2f",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b9c7995ae537fbde0778c",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b9f0195ae537fbde078bc",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "profilePicture": "https://img.clockify.me/2020-03-01T10%3A33%3A32.180Zcarroll.png",
                "activeWorkspace": "5e5b8b3a95ae537fbde06e58",
                "defaultWorkspace": "5e5b8b3a95ae537fbde06e58",
                "settings": {
                    "weekStart": "MONDAY",
                    "timeZone": "Europe/Moscow",
                    "timeFormat": "HOUR24",
                    "dateFormat": "DD/MM/YYYY",
                    "sendNewsletter": false,
                    "weeklyUpdates": false,
                    "longRunning": false,
                    "summaryReportSettings": {
                        "group": "Project",
                        "subgroup": "Time Entry"
                    },
                    "isCompactViewOn": false,
                    "dashboardSelection": "ME",
                    "dashboardViewType": "PROJECT",
                    "dashboardPinToTop": false,
                    "projectListCollapse": 50,
                    "collapseAllProjectLists": false,
                    "groupSimilarEntriesDisabled": false,
                    "myStartOfDay": "09:00",
                    "timeTrackingManual": false
                },
                "status": "ACTIVE"
            }
        """,
        200
    )
    # calling get /workspaces/<workspace id>/users
    GET_USERS = RequestMockResponse(
        """ [
            {
                "id": "5e5b91837df81c0df5f29609",
                "email": "alice_liddell_1852@list.ru",
                "name": "Alice",
                "memberships": [
                    {
                        "userId": "5e5b91837df81c0df5f29609",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b91837df81c0df5f29609",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e59",
                        "membershipType": "USERGROUP",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b91837df81c0df5f29609",
                        "hourlyRate": null,
                        "targetId": "5e5b9c7995ae537fbde0778c",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b91837df81c0df5f29609",
                        "hourlyRate": null,
                        "targetId": "5e5b9d2e95ae537fbde077e4",
                        "membershipType": "USERGROUP",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "profilePicture": "https://img.clockify.me/2020-03-01T10%3A49%3A42.471Zalice3.jpg",
                "activeWorkspace": "5e5b8b3a95ae537fbde06e58",
                "defaultWorkspace": "5e5b8b3a95ae537fbde06e58",
                "settings": {
                    "weekStart": "MONDAY",
                    "timeZone": "Europe/Moscow",
                    "timeFormat": "HOUR12",
                    "dateFormat": "MM/DD/YYYY",
                    "sendNewsletter": false,
                    "weeklyUpdates": false,
                    "longRunning": false,
                    "summaryReportSettings": {
                        "group": "Project",
                        "subgroup": "Time Entry"
                    },
                    "isCompactViewOn": false,
                    "dashboardSelection": "ME",
                    "dashboardViewType": "PROJECT",
                    "dashboardPinToTop": false,
                    "projectListCollapse": 50,
                    "collapseAllProjectLists": false,
                    "groupSimilarEntriesDisabled": false,
                    "myStartOfDay": "09:00",
                    "timeTrackingManual": false
                },
                "status": "ACTIVE"
            },
            {
                "id": "5e5b998195ae537fbde0761d",
                "email": "cheshire_cat_1788@mail.ru",
                "name": "Cheshire Cat",
                "memberships": [
                    {
                        "userId": "5e5b998195ae537fbde0761d",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "profilePicture": "https://img.clockify.me/2020-03-01T11%3A21%3A32.363ZCheshire+Cat.jpg",
                "activeWorkspace": "5e5b8b3a95ae537fbde06e58",
                "defaultWorkspace": "5e5b8b3a95ae537fbde06e58",
                "settings": {
                    "weekStart": "MONDAY",
                    "timeZone": "Europe/Moscow",
                    "timeFormat": "HOUR12",
                    "dateFormat": "MM/DD/YYYY",
                    "sendNewsletter": false,
                    "weeklyUpdates": false,
                    "longRunning": false,
                    "summaryReportSettings": {
                        "group": "Project",
                        "subgroup": "Time Entry"
                    },
                    "isCompactViewOn": false,
                    "dashboardSelection": "ME",
                    "dashboardViewType": "PROJECT",
                    "dashboardPinToTop": false,
                    "projectListCollapse": 50,
                    "collapseAllProjectLists": false,
                    "groupSimilarEntriesDisabled": false,
                    "myStartOfDay": "09:00",
                    "timeTrackingManual": false
                },
                "status": "ACTIVE"
            },
            {
                "id": "5e5b8b0a95ae537fbde06e2e",
                "email": "lewis_carroll_1832@mail.ru",
                "name": "Lewis Carroll",
                "memberships": [
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b9c7995ae537fbde0778c",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b9f0195ae537fbde078bc",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "profilePicture": "https://img.clockify.me/2020-03-01T10%3A33%3A32.180Zcarroll.png",
                "activeWorkspace": "5e5b8b3a95ae537fbde06e58",
                "defaultWorkspace": "5e5b8b3a95ae537fbde06e58",
                "settings": {
                    "weekStart": "MONDAY",
                    "timeZone": "Europe/Moscow",
                    "timeFormat": "HOUR24",
                    "dateFormat": "DD/MM/YYYY",
                    "sendNewsletter": false,
                    "weeklyUpdates": false,
                    "longRunning": false,
                    "summaryReportSettings": {
                        "group": "Project",
                        "subgroup": "Time Entry"
                    },
                    "isCompactViewOn": false,
                    "dashboardSelection": "ME",
                    "dashboardViewType": "PROJECT",
                    "dashboardPinToTop": false,
                    "projectListCollapse": 50,
                    "collapseAllProjectLists": false,
                    "groupSimilarEntriesDisabled": false,
                    "myStartOfDay": "09:00",
                    "timeTrackingManual": false
                },
                "status": "ACTIVE"
            },
            {
                "id": "5e5b94837df81c0df5f2979c",
                "email": "white_rabbit_1865@mail.ru",
                "name": "White Rabbit",
                "memberships": [
                    {
                        "userId": "5e5b94837df81c0df5f2979c",
                        "hourlyRate": null,
                        "targetId": "5e5b8b3a95ae537fbde06e58",
                        "membershipType": "WORKSPACE",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b94837df81c0df5f2979c",
                        "hourlyRate": null,
                        "targetId": "5e5b9d2e95ae537fbde077e4",
                        "membershipType": "USERGROUP",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "profilePicture": "https://img.clockify.me/2020-03-01T10%3A59%3A17.507Zwhite_rabbit.jpg",
                "activeWorkspace": "5e5b8b3a95ae537fbde06e58",
                "defaultWorkspace": "5e5b8b3a95ae537fbde06e58",
                "settings": {
                    "weekStart": "MONDAY",
                    "timeZone": "Europe/Moscow",
                    "timeFormat": "HOUR12",
                    "dateFormat": "MM/DD/YYYY",
                    "sendNewsletter": false,
                    "weeklyUpdates": false,
                    "longRunning": false,
                    "summaryReportSettings": {
                        "group": "Project",
                        "subgroup": "Time Entry"
                    },
                    "isCompactViewOn": false,
                    "dashboardSelection": "ME",
                    "dashboardViewType": "PROJECT",
                    "dashboardPinToTop": false,
                    "projectListCollapse": 50,
                    "collapseAllProjectLists": false,
                    "groupSimilarEntriesDisabled": false,
                    "myStartOfDay": "09:00",
                    "timeTrackingManual": false
                },
                "status": "ACTIVE"
            }
        ] """,
        200
    )

    # calling /workspaces/<workspace id>/projects
    GET_PROJECTS = RequestMockResponse(
        """ [
            {
                "id": "5e5b9c7995ae537fbde0778c",
                "name": "Down the Rabbit Hole",
                "hourlyRate": {
                    "amount": 0,
                    "currency": "GBP"
                },
                "clientId": "",
                "workspaceId": "5e5b8b3a95ae537fbde06e58",
                "billable": true,
                "memberships": [
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b9c7995ae537fbde0778c",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b91837df81c0df5f29609",
                        "hourlyRate": null,
                        "targetId": "5e5b9c7995ae537fbde0778c",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    },
                    {
                        "userId": "5e5b9d2e95ae537fbde077e4",
                        "hourlyRate": null,
                        "targetId": "5e5b9c7995ae537fbde0778c",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "color": "#009688",
                "estimate": {
                    "estimate": "PT0S",
                    "type": "AUTO"
                },
                "archived": false,
                "duration": "PT0S",
                "clientName": "",
                "note": "",
                "template": false,
                "public": false
            },
            {
                "id": "5e5b9f0195ae537fbde078bc",
                "name": "The Pool of Tears",
                "hourlyRate": {
                    "amount": 0,
                    "currency": "GBP"
                },
                "clientId": "",
                "workspaceId": "5e5b8b3a95ae537fbde06e58",
                "billable": true,
                "memberships": [
                    {
                        "userId": "5e5b8b0a95ae537fbde06e2e",
                        "hourlyRate": null,
                        "targetId": "5e5b9f0195ae537fbde078bc",
                        "membershipType": "PROJECT",
                        "membershipStatus": "ACTIVE"
                    }
                ],
                "color": "#FF5722",
                "estimate": {
                    "estimate": "PT0S",
                    "type": "AUTO"
                },
                "archived": false,
                "duration": "PT0S",
                "clientName": "",
                "note": "",
                "template": false,
                "public": false
            }
        ] """,
        200
    )
    GET_TASKS = RequestMockResponse(
        """ [
            {
                "id": "5e5ba93e7df81c0df5f2a1c2",
                "name": "drink me",
                "projectId": "5e5b9c7995ae537fbde0778c",
                "assigneeIds": [],
                "assigneeId": "",
                "estimate": "PT0S",
                "status": "ACTIVE",
                "duration": "PT0S"
            },
            {
                "id": "5e5ba91100352a1175bc90fa",
                "name": "eat me",
                "projectId": "5e5b9c7995ae537fbde0778c",
                "assigneeIds": [],
                "assigneeId": "",
                "estimate": "PT0S",
                "status": "ACTIVE",
                "duration": "PT0S"
            }
        ]  """,
        200
    )

    # calling post '/workspaces/<workspace id>/time-entries'
    POST_TIME_ENTRY = RequestMockResponse(
     """{"id": "123456", "description": "testing description", "tagIds": null,
     "userId": "123456", "billable": false, "taskId": null, "projectId": "123456",
     "timeInterval": {"start": "2019-10-23T17:18:58Z", "end": null, "duration": null},
     "workspaceId": "123456", "isLocked": false}
     """, 201
    )

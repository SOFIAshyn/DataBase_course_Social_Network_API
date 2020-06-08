from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.serializers import UserListSerializer, CustomerSerializer, AuthorSerializer
from accesses.serializers import AccessMessageListSerializer
from system_messages.serializers import SystemMessageListSerializer
from django.contrib.auth import get_user_model
from accesses.models import Access
from editors.models import Editor
from system_messages.models import SystemMessage
from networks.models import Network
import json
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from collections import defaultdict


User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ("role",)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects
    serializer_class = UserListSerializer


class CustomerListView(APIView):
    '''
    Task 1
    '''

    def get(self, request, id=None):
        # Example of body
        # {
        #     "date_start": "2000-11-22",
        #     "date_end": "2000-11-23",
        #     "count_of_messages": 5
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
                or "count_of_messages" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]
        count_of_messages = body["count_of_messages"]

        author_groups = get_object_or_404(User, id=id, role=1).group
        accesses = set()
        for group in author_groups.all():
            group_editors = Editor.objects.filter(group=group.id)
            for editor in group_editors:
                editor_accesses = Access.objects.filter(editor=editor.id)
                for access in editor_accesses:
                    accesses.add(access)

        customers_to_return = set()
        for access in accesses:
            messages_count = SystemMessage.objects.filter(
                access=access, date__range=(date_start, date_end)
            ).count()
            if messages_count >= count_of_messages:
                customers_to_return.add(access.customer)

        serializer = CustomerSerializer(customers_to_return, many=True)
        return Response(serializer.data, status=200)


class AuthorListView(APIView):
    '''
    Task 2
    '''

    def get(self, request, id=None):
        # Example of body
        # {
        #     "date_start": "2000-11-22",
        #     "date_end": "2000-11-23"
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]

        customer = get_object_or_404(User, id=id, role=2)
        print(customer)
        customer_accesses = Access.objects.filter(customer=customer)
        print('customer_accesses = ', customer_accesses)
        authors_to_return = set()
        for access in customer_accesses:
            messages_count = SystemMessage.objects.filter(
                access=access, date__range=(date_start, date_end)
            ).count()
            if messages_count:
                editor_groups = get_object_or_404(Editor, id=access.editor.id).group
                for group in editor_groups.all():
                    group_authors = User.objects.filter(group=group.id)
                    for author in group_authors:
                        authors_to_return.add(author)

        print('dfgchjkl; ', authors_to_return)

        serializer = AuthorSerializer(authors_to_return, many=True)
        return Response(serializer.data, status=200)


class AuthorOfDiffCustomersListView(APIView):
    '''
    Task 3
    '''

    def get(self, request):
        # Example of body
        # {
        #     "date_start": "2000-06-07T15:03:09.960533Z",
        #     "date_end": "2021-06-07T15:03:09.960533Z",
        #     "count_customers": 5
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
                or "count_customers" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]
        count_customers = body["count_customers"]

        # TODO: make api calls /customers/id/, can be done API call?
        authors_to_return = set()
        for author in User.objects.filter(role=1):
            author_groups = get_object_or_404(User, id=author.id).group
            accesses = set()
            for group in author_groups.all():
                group_editors = Editor.objects.filter(group=group.id)
                for editor in group_editors:
                    editor_accesses = Access.objects.filter(editor=editor.id)
                    for access in editor_accesses:
                        accesses.add(access)

            author_customers = set()
            for access in accesses:
                messages_count = SystemMessage.objects.filter(
                    access=access, date__range=(date_start, date_end)
                ).count()
                if messages_count:
                    author_customers.add(access.customer)

            if len(author_customers) > count_customers:
                authors_to_return.add(author)

        serializer = AuthorSerializer(authors_to_return, many=True)
        return Response(serializer.data, status=200)


class CustomerOfDiffMessagesListView(APIView):
    '''
    Task 4
    '''

    def get(self, request):
        # Example of body
        # {
        #     "date_start": "2000-06-07T15:03:09.960533Z",
        #     "date_end": "2021-06-07T15:03:09.960533Z",
        #     "count_messages": 5
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
                or "count_messages" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]
        count_messages = body["count_messages"]

        customers_to_return = set()
        for customer in User.objects.filter(role=2):
            customer_accesses = Access.objects.filter(customer=customer.id)
            for access in customer_accesses:
                messages_count = SystemMessage.objects.filter(
                    access=access, date__range=(date_start, date_end)
                ).count()
                if messages_count >= count_messages:
                    customers_to_return.add(access.customer)

        serializer = CustomerSerializer(customers_to_return, many=True)
        return Response(serializer.data, status=200)


class SocialsListView(APIView):
    '''
    Task 5
    '''
    SOCIALS = (
        (1, 'Instagram'),
        (2, 'Facebook'),
        (3, 'Telegram')
    )

    def get(self, request, id=None):
        # Example of body
        # {
        #     "date_start": "2000-06-07T15:03:09.960533Z",
        #     "date_end": "2021-06-07T15:03:09.960533Z",
        #     "count_orders": 5
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
                or "count_orders" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]
        count_orders = body["count_orders"]

        customer = get_object_or_404(User, id=id, role=2)
        socials_to_return = defaultdict()
        num_of_socials = len(self.SOCIALS)
        for soc_id in range(1, num_of_socials + 1):
            customer_accesses = Access.objects.filter(customer=customer.id, social_name=soc_id)
            for access in customer_accesses:
                messages_count = SystemMessage.objects.filter(
                    access=access, date__range=(date_start, date_end)
                ).count()
                if messages_count >= count_orders:
                    socials_to_return[self.SOCIALS[soc_id - 1][1]] = messages_count

        return JsonResponse(socials_to_return)


class AuthorsSocialsListView(APIView):
    '''
    Task 6
    '''
    def get(self, request, id=None):
        # Example of body
        # {
        #     "date_start": "2000-06-07T15:03:09.960533Z",
        #     "date_end": "2021-06-07T15:03:09.960533Z"
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]

        author_groups = get_object_or_404(User, id=id, role=1).group
        accounts_to_return = defaultdict()
        for group in author_groups.all():
            group_editors = Editor.objects.filter(group=group.id)
            for editor in group_editors:
                editor_accesses = Access.objects.filter(editor=editor.id, date_start__lte=date_end, \
                                                        date_end__gte=date_start)
                for access in editor_accesses:
                    access_customer_id = access.customer.id  # 4 - max
                    access_network_id = access.social_name  # 1 - inst
                    # all users networks that author has an access to
                    users_network_ids = get_object_or_404(User, id=access_customer_id).networks
                    if users_network_ids is not None:
                        netw = users_network_ids.get_id()
                        if access_network_id == 1:
                            accounts_to_return['Instagram'] = get_object_or_404(Network, id=netw).inst_username
                        if access_network_id == 2:
                            accounts_to_return['Facebook'] = get_object_or_404(Network, id=netw).fb_username
                        if access_network_id == 3:
                            accounts_to_return['Telegram'] = get_object_or_404(Network, id=netw).tg_username

        return JsonResponse(accounts_to_return)


class AccessDeniedListView(APIView):
    '''
    Task 7
    '''
    def get(self, request, id=None):
        customer = get_object_or_404(User, id=id, role=2)
        customer_accesses = Access.objects.filter(customer=customer.id)
        denied_accesses_editors = set()
        for access_init in customer_accesses:
            same_queries = Access.objects.filter(social_name=access_init.social_name, \
                                                customer=access_init.customer, \
                                                editor=access_init.editor, \
                                                date_start=access_init.date_start
                                                )

            if [el.id for el in sorted(same_queries, key=lambda access: access.id, reverse=True)] != \
            [el.id for el in sorted(same_queries, key=lambda access: access.date_end, reverse=True)]:
                denied_accesses_editors.add(same_queries[0].editor)

        denied_authors_to_return = set()
        for editor in denied_accesses_editors:
            editor_groups = get_object_or_404(Editor, id=editor.id).group
            for group in editor_groups.all():
                group_authors = User.objects.filter(group=group.id, role=1)
                for author in group_authors:
                    denied_authors_to_return.add(author)

        serializer = AuthorSerializer(denied_authors_to_return, many=True)
        return Response(serializer.data, status=200)


class CommonEventsListView(APIView):
    '''
    Task 8
    '''
    def get(self, request, author_id=None, customer_id=None):
        # Example of body
        # {
        #     "date_start": "2000-06-07T15:03:09.960533Z",
        #     "date_end": "2021-06-07T15:03:09.960533Z"
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]

        author_groups = get_object_or_404(User, id=author_id, role=1).group
        customer = get_object_or_404(User, id=customer_id, role=2)
        customer_accesses = set(Access.objects.filter(customer=customer.id, date_start__lte=date_end, \
                                                      date_end__gte=date_start))
        author_accesses = set()
        for group in author_groups.all():
            group_editors = Editor.objects.filter(group=group.id)
            for editor in group_editors:
                editor_accesses = Access.objects.filter(editor=editor.id, date_start__lte=date_end, \
                                                        date_end__gte=date_start)
                for access in editor_accesses:
                    author_accesses.add(access)

        common_accesses = customer_accesses.intersection(author_accesses)

        access_serializer = AccessMessageListSerializer(common_accesses, many=True)
        return Response(access_serializer.data, status=200)


# class AuthorGroupSize(APIView):
#     '''
#     Task 9
#     '''
#     def get(self, request, id=None):
#         # Example of body
#         # {
#         #     "date_start": "2000-06-07T15:03:09.960533Z",
#         #     "date_end": "2021-06-07T15:03:09.960533Z"
#         # }
#         try:
#             body = json.loads(request.body)
#         except:
#             return Response(status=400)
#         if (
#                 "date_start" not in body
#                 or "date_end" not in body
#         ):
#             return Response(status=400)
#
#         date_start = body["date_start"]
#         date_end = body["date_end"]





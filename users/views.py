from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.serializers import UserListSerializer, CustomerSerializer, AuthorSerializer
from accesses.serializers import AccessMessageListSerializer, AccessListSerializer
from groups.serializers import GroupListSerializer
from groups.models import Group
from django.contrib.auth import get_user_model
from accesses.models import Access
from editors.models import Editor
from system_messages.models import SystemMessage
from networks.models import Network
import json
from django_filters.rest_framework import DjangoFilterBackend
from collections import defaultdict, OrderedDict
import datetime
import monthdelta
import pytz
# from rest_framework.permissions import IsAuthenticated

utc=pytz.UTC

User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ("role", )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects
    serializer_class = UserListSerializer


class CustomerListView(APIView):
    '''
    Task 1
    '''
    # permission_classes = (IsAuthenticated,)

    def post(self, request, id=None):
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

    def post(self, request, id=None):
        # Example of body
        {
            "date_start": "2000-11-22",
            "date_end": "2000-11-23"
        }
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
        customer_accesses = Access.objects.filter(customer=customer)
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

        serializer = AuthorSerializer(authors_to_return, many=True)
        return Response(serializer.data, status=200)


class AuthorOfDiffCustomersListView(APIView):
    '''
    Task 3
    '''

    def post(self, request):
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

    def post(self, request):
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

    def post(self, request, id=None):
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

        return Response(socials_to_return, status=200)


class AuthorsSocialsListView(APIView):
    '''
    Task 6
    '''
    def post(self, request, id=None):
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

        return Response(accounts_to_return, status=200)


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
    def post(self, request, author_id=None, customer_id=None):
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


class AuthorGroupSizeListView(APIView):
    '''
    Task 9
    '''
    SOCIALS = (
        (1, 'Instagram'),
        (2, 'Facebook'),
        (3, 'Telegram')
    )

    def post(self, request, id=None):
        # Example of body
        # {
        #     "date_start": "2000-06-07T15:03:09.960533Z",
        #     "date_end": "2021-06-07T15:03:09.960533Z",
        #     "count_authors": 4
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "date_start" not in body
                or "date_end" not in body
                or "count_authors" not in body
        ):
            return Response(status=400)

        date_start = body["date_start"]
        date_end = body["date_end"]
        count_authors = body["count_authors"]

        author_messages_to_return = defaultdict()
        author_groups = get_object_or_404(User, id=id, role=1).group
        for group in author_groups.all():
            if len(User.objects.filter(group=group.id)) >= count_authors:
                group_editors = Editor.objects.filter(group=group.id)
                for editor in group_editors:
                    for soc_id in range(1, len(self.SOCIALS) + 1):
                        editor_soc_accesses = Access.objects.filter(editor=editor.id, date_start__lte=date_end, \
                                                                date_end__gte=date_start, social_name=soc_id)
                        for access in editor_soc_accesses:
                            messages_count = SystemMessage.objects.filter(
                                access=access, date__range=(date_start, date_end)
                            ).count()
                            if messages_count:
                                author_messages_to_return[self.SOCIALS[soc_id - 1][1]] = messages_count

        return Response(author_messages_to_return, status=200)


class CustomerStyleListView(APIView):
    '''
    Task 10
    '''
    def post(self, request, id=None):
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

        customer = get_object_or_404(User, id=id, role=2)
        customer_accesses = Access.objects.filter(customer=customer, date_start__lte=date_end, \
                                                  date_end__gte=date_start)
        sale_orders_to_return = {}
        for access in customer_accesses:
            editor = get_object_or_404(Editor, id=access.editor.id)
            if editor.sale is not None:
                sale_start = editor.sale_started
                sale_end = editor.sale_started.date() + datetime.timedelta(days=int(editor.sale.duration))
                messages = SystemMessage.objects.filter(
                    access=access, date__range=(sale_start, sale_end)
                )
                for message in messages:
                    if message.style not in sale_orders_to_return.keys():
                        sale_orders_to_return[message.get_style()] = 0
                    sale_orders_to_return[message.get_style()] += 1

        return Response(sale_orders_to_return, status=200)


class MonthlyOrdersListView(APIView):
    '''
    Task 11
    '''
    def get(self, request):
        # naive
        start_date = SystemMessage.objects.latest('date').get_date()
        end_date = datetime.datetime.now()

        monthly_to_return = {}
        all_months = 0
        while not all_months:
            month_end_date = start_date + monthdelta.monthdelta(1)
            month_end_date = month_end_date.replace(tzinfo=utc)
            end_date = end_date.replace(tzinfo=utc)
            start_date = start_date.replace(tzinfo=utc)
            if month_end_date > end_date:
                month_end_date = end_date
                all_months = 1
            messages_count = SystemMessage.objects.filter(date__range=(start_date, month_end_date)).count()
            if start_date.strftime('%B') not in monthly_to_return.keys():
                monthly_to_return[start_date.strftime('%B')] = 0
            monthly_to_return[start_date.strftime('%B')] += messages_count
            start_date = month_end_date

        return Response(monthly_to_return, status=200)


class ActiveNetworksListView(APIView):
    '''
    Task 12
    '''
    def post(self, request, id=None):
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
        author_net_messages = {}
        for group in author_groups.all():
            group_editors = Editor.objects.filter(group=group.id)
            for editor in group_editors:
                editor_accesses = Access.objects.filter(editor=editor.id, date_start__lte=date_end, \
                                                  date_end__gte=date_start)
                for access in editor_accesses:
                    network = access.get_network_name()
                    if network not in author_net_messages.keys():
                        author_net_messages[network] = {}
                    messages = SystemMessage.objects.filter(
                        access=access, date__range=(date_start, date_end)
                    )
                    for message in messages:
                        if message.get_style() not in author_net_messages[network].keys():
                            author_net_messages[network][message.get_style()] = 0
                        author_net_messages[network][message.get_style()] += 1
        author_net_average = defaultdict()
        for name, data in author_net_messages.items():
            messages_num = 0
            for message_data in data.values():
                messages_num += message_data
            if messages_num != 0:
                author_net_average[name] = messages_num / len(author_net_messages)
        return Response(OrderedDict(sorted(author_net_average.items(), key=lambda net_messages: net_messages[1], reverse=True)), status=200)


class UserDataListView(APIView):
    def post(self, request):
        # Example of body
        # {
        #     "username": "anna_petryshyn",
        #     "password": "anna_pass"
        # }
        try:
            body = json.loads(request.body)
        except:
            return Response(status=400)
        if (
                "username" not in body
                or "password" not in body
        ):
            return Response(status=400)

        username = body["username"]
        password = body["password"]

        user = get_object_or_404(User, username=username)

        # serializer = LoggedInUserSerializer(user)
        return Response({'id': user.id, 'e-mail': user.email, 'role': user.role}, status=200)


class UserAuthorLastAccessListView(APIView):
    '''
    Task 3 from the 1 part
    '''
    def get(self, request, customer_id=None, editor_id=None):
        customer = get_object_or_404(User, id=customer_id, role=2)
        editor = get_object_or_404(User, id=editor_id, role=1)

        accesses = Access.objects.filter(customer=customer.id, editor=editor.id).last()

        serializer = AccessListSerializer(accesses)
        return Response(serializer.data, status=200)


class AuthorGroupsListView(generics.ListAPIView):
    queryset = Group.objects
    serializer_class = GroupListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.filter(participants__exact=self.kwargs['id'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

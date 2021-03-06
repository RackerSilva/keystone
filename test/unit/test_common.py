import os
import sys
# Need to access identity module
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),
                                '..', '..', '..', '..', 'keystone')))
import unittest
from webtest import TestApp
import httplib2
import json
from lxml import etree


URL = 'http://localhost:8080/v1.0/'


def get_token(user, pswd, kind='', tenant_id=None):
    header = httplib2.Http(".cache")
    url = '%stoken' % URL
    if not tenant_id:
        body = {"passwordCredentials": {"username": user,
                                        "password": pswd}}
    else:
        body = {"passwordCredentials": {"username": user,
                                        "password": pswd,
                                        "tenantId": tenant_id}}

    resp, content = header.request(url, "POST", body=json.dumps(body),
                              headers={"Content-Type": "application/json"})
    content = json.loads(content)
    token = str(content['auth']['token']['id'])
    if kind == 'token':
        return token
    else:
        return (resp, content)


def delete_token(token, auth_token):
    header = httplib2.Http(".cache")
    url = '%stoken/%s' % (URL, token)
    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def create_tenant(tenantid, auth_token):
    header = httplib2.Http(".cache")

    url = '%stenants' % (URL)
    body = {"tenant": {"id": tenantid,
                       "description": "A description ...",
                       "enabled": True}}
    resp, content = header.request(url, "POST", body=json.dumps(body),
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def create_tenant_group(groupid, tenantid, auth_token):
    header = httplib2.Http(".cache")

    url = '%stenant/%s/groups' % (URL, tenantid)
    body = {"group": {"id": groupid,
                       "description": "A description ..."}}
    resp, content = header.request(url, "POST", body=json.dumps(body),
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def delete_tenant(tenantid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s' % (URL, tenantid)
    resp, content = header.request(url, "DELETE", body='{}',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def delete_tenant_group(groupid, tenantid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenant/%s/groups/%s' % (URL, tenantid, groupid)
    resp, content = header.request(url, "DELETE", body='{}',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def create_global_group(groupid, auth_token):
    header = httplib2.Http(".cache")

    url = '%sgroups' % (URL)
    body = {"group": {"id": groupid,
                       "description": "A description ..."}}
    resp, content = header.request(url, "POST", body=json.dumps(body),
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def create_global_group_xml(groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups' % (URL)
    body = '<?xml version="1.0" encoding="UTF-8"?>\
            <group xmlns="http://docs.openstack.org/idm/api/v1.0" \
            id="%s"><description>A Description of the group</description>\
                    </group>' % groupid
    resp, content = header.request(url, "POST", body=body,
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def delete_global_group(groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s' % (URL, groupid)
    resp, content = header.request(url, "DELETE", body='{}',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def delete_global_group_xml(groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s' % (URL, groupid)
    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def get_token_xml(user, pswd, type='', tenant_id=None):
        header = httplib2.Http(".cache")
        url = '%stoken' % URL
        if tenant_id:
            body = '<?xml version="1.0" encoding="UTF-8"?> \
                    <passwordCredentials \
                    xmlns="http://docs.openstack.org/idm/api/v1.0" \
                    password="%s" username="%s" \
                    tenantId="%s"/> ' % (pswd, user, tenant_id)
        else:
            body = '<?xml version="1.0" encoding="UTF-8"?> \
                    <passwordCredentials \
                    xmlns="http://docs.openstack.org/idm/api/v1.0" \
                    password="%s" username="%s" /> ' % (pswd, user)
        resp, content = header.request(url, "POST", body=body,
                                  headers={"Content-Type": "application/xml",
                                         "ACCEPT": "application/xml"})
        dom = etree.fromstring(content)
        root = dom.find("{http://docs.openstack.org/idm/api/v1.0}token")
        token_root = root.attrib
        token = str(token_root['id'])
        if type == 'token':
            return token
        else:
            return (resp, content)


def delete_token_xml(token, auth_token):
    header = httplib2.Http(".cache")
    url = '%stoken/%s' % (URL, token)
    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def create_tenant_xml(tenantid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants' % (URL)
    body = '<?xml version="1.0" encoding="UTF-8"?> \
            <tenant xmlns="http://docs.openstack.org/idm/api/v1.0" \
            enabled="true" id="%s"> \
            <description>A description...</description> \
            </tenant>' % tenantid
    resp, content = header.request(url, "POST", body=body,
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def create_tenant_group_xml(groupid, tenantid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenant/%s/groups' % (URL, tenantid)
    body = '<?xml version="1.0" encoding="UTF-8"?> \
            <group xmlns="http://docs.openstack.org/idm/api/v1.0" \
             id="%s"> \
            <description>A description...</description> \
            </group>' % groupid
    resp, content = header.request(url, "POST", body=body,
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def delete_tenant_xml(tenantid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s' % (URL, tenantid)
    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def delete_tenant_group_xml(groupid, tenantid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenant/%s/groups/%s' % (URL, tenantid, groupid)
    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def create_user(tenantid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/users' % (URL, tenantid)
    body = {"user": {"password": "secrete",
                     "id": userid,
                     "tenantId": tenantid,
                     "email": "%s@rackspace.com" % userid,
                     "enabled": True}}
    resp, content = header.request(url, "POST", body=json.dumps(body),
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def delete_user(tenant, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/users/%s' % (URL, tenant, userid)

    resp, content = header.request(url, "DELETE", body='{}',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})

    return (resp, content)


def create_user_xml(tenantid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/users' % (URL, tenantid)
    body = '<?xml version="1.0" encoding="UTF-8"?> \
            <user xmlns="http://docs.openstack.org/idm/api/v1.0" \
            email="joetest@rackspace.com" \
            tenantId="%s" id="%s" \
            enabled="true" password="secrete"/>' % (tenantid, userid)
    resp, content = header.request(url, "POST", body=body,
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def delete_user_xml(tenantid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/users/%s' % (URL, tenantid, userid)
    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def add_user_tenant_group(tenantid, groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/groups/%s/users/%s' % (URL, tenantid, groupid, userid)

    resp, content = header.request(url, "PUT", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def add_user_tenant_group_xml(tenantid, groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/groups/%s/users/%s' % (URL, tenantid, groupid, userid)

    resp, content = header.request(url, "PUT", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def delete_user_tenant_group(tenantid, groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/groups/%s/users/%s' % (URL, tenantid, groupid, userid)

    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def delete_user_tenant_group_xml(tenantid, groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/groups/%s/users/%s' % (URL, tenantid, groupid, userid)

    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def get_user_tenant_group(tenantid, groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/groups/%s/users' % (URL, tenantid, groupid)

    resp, content = header.request(url, "GET", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def get_user_tenant_group_xml(tenantid, groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%stenants/%s/groups/%s/users' % (URL, tenantid, groupid)

    resp, content = header.request(url, "GET", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def add_user_global_group(groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s/users/%s' % (URL, groupid, userid)

    resp, content = header.request(url, "PUT", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def add_user_global_group_xml(groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s/users/%s' % (URL, groupid, userid)

    resp, content = header.request(url, "PUT", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def delete_user_global_group(groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s/users/%s' % (URL, groupid, userid)

    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})
    return (resp, content)


def delete_user_global_group_xml(groupid, userid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s/users/%s' % (URL, groupid, userid)

    resp, content = header.request(url, "DELETE", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def get_user_global_group(groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s/users' % (URL, groupid)

    resp, content = header.request(url, "GET", body='',
                              headers={"Content-Type": "application/json",
                                       "X-Auth-Token": auth_token})

    return (resp, content)


def get_userid():
    return 'test_user11'


def get_password():
    return 'secrete'


def get_email():
    return 'joetest@rackspace.com'


def get_user_global_group_xml(groupid, auth_token):
    header = httplib2.Http(".cache")
    url = '%sgroups/%s/users' % (URL, groupid)

    resp, content = header.request(url, "GET", body='',
                              headers={"Content-Type": "application/xml",
                                       "X-Auth-Token": auth_token,
                                       "ACCEPT": "application/xml"})
    return (resp, content)


def get_tenant():
    return '1234'


def get_user():
    return 'test_user'


def get_userdisabled():
    return 'disabled'


def get_auth_token():
    return '999888777666'


def get_exp_auth_token():
    return '000999'


def get_none_token():
    return ''


def get_non_existing_token():
    return 'invalid_token'


def get_disabled_token():
    return '999888777'


def content_type(resp):
    return resp['content-type'].split(';')[0]


def get_global_tenant():
    return 'GlobalTenant'


def handle_user_resp(self, content, respvalue, resptype):
    if respvalue == 200:
        if resptype == 'application/json':
            content = json.loads(content)
            self.tenant = content['user']['tenantId']
            self.userid = content['user']['id']
        if resptype == 'application/xml':
            content = etree.fromstring(content)
            self.tenant = content.get("tenantId")
            self.id = content.get("id")

    if respvalue == 500:
        self.fail('IDM fault')
    elif respvalue == 503:
        self.fail('Service Not Available')


def content_type(resp):
    return resp['content-type'].split(';')[0]

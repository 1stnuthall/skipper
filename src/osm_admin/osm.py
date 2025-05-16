''' OSM Class. '''
import requests, json, time, logging, re
from datetime import datetime
import pickle, re

from .config import *
from .login import headers
from utils import get_cache, write_cache

class OSM:
    def __init__(self, section_name) -> None:

        # Get Section ID and Group from Roles
        for role in self.get_user_roles():
            if role['section'] == section_name:
                section_id = role['sectionid']
                section_group = role['groupname'].replace(section_name.title(), '').strip()

        # # Get basic Section Details
        self.name = section_name
        self.id = section_id
        self.group = section_group
        self.current_term = self.get_current_term()
        self.size = self.scouts()['count']

    def __str__(self):
        return f"{self.group}"
    
    def post(self, url, scope, cachefile = None, data = None, json_output = True):
        cache = get_cache(cachefile)
        if not cache or cachefile == None:
            response = requests.post(url = url, headers = headers, data = data)
            print("post")
            if int(response.headers._store['x-ratelimit-remaining'][1]) < 300:
                raise Exception(f"Rate limit dangerously low ({response.headers._store['x-ratelimit-remaining'][1]}), stopping")

            if response.status_code == 429:
                print("Too many requests, sleeping")
                time.sleep(int(response.headers._store['retry-after'][1])+2)
                response = requests.post(url = url, headers = headers, data = data)

            if response.status_code != 200:
                raise Exception("OSM Request failed:", response.status_code, response.text)
            
            if json_output:
                response = json.loads(response.content)

            if not cachefile == None:
                write_cache(cachefile, response)

            return response
        else:
            return cache

    def get(self, url, cachefile = None, json_output = True):
        cache = get_cache(cachefile)
        if not cache or cachefile == None:
            response = requests.get(url = url, headers = headers)
            print("get")
            # if int(response.headers._store['x-ratelimit-remaining'][1]) < 30:
            #     raise Exception(f"Rate limit dangerously low ({response.headers._store['x-ratelimit-remaining'][1]}), stopping")

            if response.status_code == 429:
                print("Too many requests, sleeping")
                time.sleep(int(response.headers._store['retry-after'][1])+2)
                response = requests.get(url = url, headers = headers)

            if response.status_code != 200:
                raise Exception("OSM Request failed:", response.status_code, response.text)
            
            if json_output:
                response = json.loads(response.content)

            if not cachefile == None:
                write_cache(cachefile, response)

            return response
        else:
            return cache

    def scouts(self):
        url = f'{OSM_BASE_URL}/ext/members/contact/?action=getListOfMembers&sort=lastname&sectionid={self.id}&termid={self.current_term}&section={self.name}'
        data = self.get(url = url, cachefile = f'{self.id}_scouts')['items']

        scouts = list()
        size = 0
        for scout in data:
            if int(scout['patrolid']) > 0:
                size += 1
                scouts.append({
                    "scoutid": str(scout['scoutid']),
                    "firstname": scout['firstname'],
                    "lastname": scout['lastname'],
                    "photo_guid": scout['photo_guid'],
                    "patrolid": scout['patrolid'],
                    "patrol": scout['patrol'],
                    "patrol_role_level_label": scout['patrol_role_level_label'],
                    "active": scout['active'],
                    "full_name": scout['full_name'].replace("  ", " ").strip()
                })
                
        return(dict({
            "count": size,
            "scouts": scouts
        }))
    
    def scouts_contacts(self):
        contact_list = dict()
        for scout in self.scouts()['scouts']:
            url = f'{OSM_BASE_URL}/ext/customdata/?action=getData&section_id={self.id}&associated_id={scout['scoutid']}&associated_type=member&associated_is_section=null&varname_filter=null&context=members&group_order=section'
            data = self.get(url = url, cachefile = f'{self.id}_{scout['scoutid']}_scout_contacts')['data']

            contacts = list()
            for contact in data:
                if re.search(r"^contact_primary_\d$", contact['identifier']):
                    contacts.append({
                        item['varname']: item['value'] for item in contact['columns'] if item['value'] not in [None, "None", ""]
                    })

            phone_numbers = list()
            for contact in contacts:
                for key in contact:
                    if key.endswith("_sms") and contact[key] == "yes" and key.replace("_sms", "") in contact:
                        phone_numbers.append(contact[key.replace("_sms", "")].replace(" ", "").replace("0", "+44", 1).strip())

            email_addresses = list()
            for contact in contacts:
                for key in contact:
                    if key.startswith("email"):
                        email_addresses.append(contact[key].replace(" ", "").lower().strip())

            contact_list.update({
                scout['scoutid']: {
                    "name": scout['full_name'],
                    # "contacts": contacts,
                    "text_messages": phone_numbers,
                    "email_addresses": email_addresses
                }
            })
        
        return(contact_list)
    
    def patrols(self, include_no_patrol = "n"):
        url = f'{OSM_BASE_URL}/ext/members/patrols?action=getPatrolsWithPeople&sectionid={self.id}&termid={self.current_term}&include_no_patrol={include_no_patrol}'
        data = self.get(url = url, cachefile = f'{self.id}_patrols')['items']

        patrols = list()
        size = 0
        for patrol in data:
            if patrol['active'] == "1" and not patrol['name'].contains("Leader", "New") :
                size += 1
                patrols.append({
                    "patrolid": patrol['patrolid'],
                    "name": patrol['name'],
                    "points": patrol['lastname'],
                    "members": patrol['members']
                })
                
        return(dict({
            "count": size,
            "patrols": patrols
        }))
    
    def get_terms(self):
        url = f'{OSM_BASE_URL}/api.php?action=getTerms&section_id={self.id}&section={self.name}'
        return self.get(url = url, cachefile = f'{self.id}_terms')
    
    def get_term(self, term_id):
        for term in self.get_terms()[self.id][::-1]:
            if term['termid'] == term_id:
                return term

    def get_current_term(self):
        terms = self.get_terms()[self.id]
        for term in terms[::-1]:
            startdate = [int(date) for date in term['startdate'].split('-')]
            enddate   = [int(date) for date in term['enddate'].split('-')]
            term_start = datetime(startdate[0], startdate[1], startdate[2])
            term_end   = datetime(enddate[0], enddate[1], enddate[2])
            if datetime.today() >= term_start and datetime.today() <= term_end:
                return term['termid']
        return terms[-1]['termid']

    def create_flexi_column(self, extraid, column_name):
        url = f'{OSM_BASE_URL}/ext/members/flexirecords/?action=addColumn&sectionid={self.id}&extraid={extraid}'
        data = {
            "columnName": column_name
        }
        column_config = self.post(url = url, data = data)['config']
        return json.loads(column_config)[0]['id']

    def create_flexi_record(self, flexi_record_name, type = 'maths'):
        url = f'{OSM_BASE_URL}/ext/members/flexirecords/?action=addRecordSet&sectionid={self.id}'
        data = {
            "name":	flexi_record_name,
            "type": type
        }
        return self.post(url = url, data = data)['id']

    def badges(self):
        badges = list()
        chief_scout_badge = ""
        for badge_type in range(1,4):
            badges.update({BADGE_TYPE[badge_type]: {}})

        badge_details = self.get_badge_structure_by_type(badge_type)['details']
        for badge_id, badge_detail in badge_details.items():
            # Separate Chief Scout Badge
            if re.search('chief', badge_detail['name'], re.IGNORECASE):
                chief_scout_badge = dict({
                    "identifier": badge_detail['badge_identifier'],
                    "name": badge_detail['name'],
                    "version": badge_detail['badge_version'],
                    "id": badge_id,
                    "picture": badge_detail['picture'],
                    "description": badge_detail['description']
                })

            else:
                badges[BADGE_TYPE[badge_type]].append({
                    "identifier": badge_detail['badge_identifier'],
                    "name": badge_detail['name'],
                    "version": badge_detail['badge_version'],
                    "id": badge_id,
                    "picture": badge_detail['picture'],
                    "description": badge_detail['description']
                })
        return dict({
            "chief_scout_badge": chief_scout_badge,
            "challenge": badges[1],
            "activity": badges[2],
            "staged": badges[3]
        })
                    
    def get_badges_flexi(self, flexi_record_name):
        url = f'{OSM_BASE_URL}/ext/members/flexirecords/?action=getFlexiRecords&sectionid={self.id}&archived=n'
        flexi_records = self.get(url = url, cachefile = f'{self.id}_{flexi_record_name}')
        
        # Create object to pass out
        badges_flexi_record = {'knots': {}}
        for flexi_record in flexi_records['items']:
            if flexi_record['name'] == flexi_record_name:
                badges_flexi_record.update({'extraid':flexi_record['extraid']})
                url = f"{OSM_BASE_URL}/ext/members/flexirecords/?action=getStructure&sectionid={self.id}&extraid={flexi_record['extraid']}"
                flexi_structure = self.get(url = url, cachefile = f'{self.id}_{flexi_record_name}')['items']
                #flexi_structure = json.loads(flexi_config)
                for col in flexi_structure:
                    if col['name'] == "Activity Badges":
                        badges_flexi_record.update({'activity_badges':col['id']})
                    elif col['name'] == "Staged Badges":
                        badges_flexi_record.update({'staged_badges':col['id']})
                    elif col['name'] == "Shoelace":
                        badges_flexi_record['knots'].update({'shoelace':col['id']})
                    elif col['name'] == "Reef Knot":
                        badges_flexi_record['knots'].update({'reef':col['id']})

        # Create the Flexi Record if it doesn't exist
        if len(badges_flexi_record) == 0:
            flexi_id = self.create_flexi_record(BADGE_FLEXI_NAME)
            badges_flexi_record = {
                'extraid': flexi_id,
                'activity_badges': self.create_flexi_column(self.id, flexi_id, "Activity Badges"),
                'staged_badges': self.create_flexi_column(self.id, flexi_id, "Staged Badges")
            }

        return badges_flexi_record
            
    def get_flexi_record_structure(self, extraid):
        url = f'{OSM_BASE_URL}/ext/members/flexirecords//?action=getStructure&extraid={extraid}&sectionid={self.id}'
        return self.get(url = url, scope = 'flexi')

    def get_flexi_record_by_id(self, extraid):
        url = f'{OSM_BASE_URL}/ext/members/flexirecords/?action=getData&extraid={extraid}&sectionid={self.id}&termid={self.current_term}&nototal'
        flexi_record = {'extraid':extraid}
        flexi_record.update(self.get(url = url, cachefile = f"{self.id}_{extraid}"))
        flexi_record.update({'config':self.get_flexi_column_config(flexi_record['extraid'])})
        return flexi_record
    
    def get_flexi_record_by_name(self, name, create = False, type = 'maths'):
        for record in self.get_all_flexi_records():
            if record['name'] == name:
                return self.get_flexi_record_by_id(record['extraid'], name)
        if create:
            return self.get_flexi_record_by_id(self.create_flexi_record(name, type))
    
    def get_flexi_record_id(self, name, create = False, type = 'maths'):
        for record in self.get_all_flexi_records():
            if record['name'] == name:
                return record['extraid']
        if create:
            return self.create_flexi_record(name, type)
        
    def get_flexi_column_config(self, flexi_record, flexi_record_name):
        url = f"{OSM_BASE_URL}/ext/members/flexirecords/?action=getStructure&sectionid={self.id}&extraid={flexi_record}"
        return self.get(url = url, cachefile = f'{self.id}_{flexi_record_name}')['items']

    def get_all_flexi_records(self):
        url = f'https://www.onlinescoutmanager.co.uk/ext/members/flexirecords/?action=getFlexiRecords&sectionid={self.id}&archived=n'
        return self.get(url = url, cachefile = f'{self.id}_flexi_records')['items']

    def get_badge_column_id(self, badge_id, badge_type, column_name):
        badge_structure = self.get_badge_structure_by_type(badge_type)['structure']
        for id, badge in badge_structure.items():
            if id == badge_id:
                for row in badge[1]['rows']:
                    if row['name'] == column_name:
                        return row['field']

    def get_badge_records_by_member(self):
        url = f'{OSM_BASE_URL}/ext/badges/badgesbyperson/?action=loadBadgesByMember&section={self.name}&sectionid={self.id}&term_id={self.current_term}'
        return self.get(url = url, cachefile = f'{self.id}_badge_completion')
    
    def split_badge_identifier(badge_identifier = None, badge_id = None, badge_version = None):
        if badge_identifier != None:
            badge_id = badge_identifier.split('_')[0]
            badge_version = badge_identifier.split('_')[1]

        return dict({
            "id": badge_id,
            "version": badge_version
        })

    def get_badge_record(self, badge_name, badge_identifier = None, badge_id = None, badge_version = None):
        badge = self.split_badge_identifier(badge_identifier, badge_id, badge_version)

        url = f'{OSM_BASE_URL}/ext/badges/records/?action=getBadgeRecords&term_id={self.current_term}&section={self.name}&badge_id={badge["id"]}&section_id={self.id}&badge_version={badge["version"]}'
        return self.get(url = url, cachefile = f'{self.id}_{badge["id"]}_{badge_name}')
    
    def get_badge_record_by_identifier(self, badge_name, badge_identifier = None, badge_id = None, badge_version = None):
        badge = self.split_badge_identifier(badge_identifier, badge_id, badge_version)

        url = f'{OSM_BASE_URL}/ext/badges/records/?action=getBadgeRecords&term_id={self.current_term}&section={self.name}&badge_id={badge["id"]}&section_id={self.id}&badge_version={badge["version"]}'
        return self.get(url = url, cachefile = f'{self.id}_{badge_name}')

    def get_user_roles(self):
        return self.get(url = ROLES_URL, cachefile = 'roles')

    def get_badge_structure_by_type(self, type_id):
        url = f'{OSM_BASE_URL}/ext/badges/records/?action=getBadgeStructureByType&a=1&section={self.name}&type_id={type_id}&term_id={self.current_term}&section_id={self.id}'
        return self.get(url = url, cachefile = f'{self.id}_badge_{BADGE_TYPE[type_id]}')

    def update_flexi_record(self, extraid, scout, column, value):
        data = {
            "extraid": extraid,
            "termid": self.current_term,
            "section": self.name,
            "sectionid": self.id,
            "scoutid": scout,
            "column": column,
            "value": value
        }
        return self.post(url = FLEXI_URL, data = data, cachefile = f'{self.id}_{extraid}')

    def update_badge_record(self, data):
        return self.post(url = BADGE_URL, data = data, cachefile = f'{self.id}_badge_record')

    def get_programme_summary(self):
        url = f"{OSM_BASE_URL}/ext/programme/?action=getProgrammeSummary&sectionid={self.id}&termid={self.current_term}"
        return self.get(url = url, cachefile = f'{self.id}_programme_summary')
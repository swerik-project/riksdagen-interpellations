#!/usr/bin/env python3
"""
Test quality of the preface.
"""
from glob import glob
from lxml import etree
from pyriksdagen.utils import (
    parse_protocol,
)
from tqdm import tqdm
import os, unittest, warnings




class Test(unittest.TestCase):

    def _fetch_data_paths(self):
        return sorted(list(glob("data/*/*.xml")))


    #@unittest.skip
    def test_ttitleStmt_author(self):
        ipqs = self._fetch_data_paths()
        bad_freetext_title = 0
        missing_titles = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            author_t = root.find(f".//{t}titleStmt/{t}author")
            if author_t is None or (author_t.text is None or author_t.text == ''):
                bad_freetext_title += 1
                missing_titles.append(ipq)

        if bad_freetext_title > 0:
            print("\n¡¡BAD!! Author in titleStatment:",
                  str(bad_freetext_title), "of", str(len(ipqs)), "|",
                  str(bad_freetext_title/len(ipqs)),
                  "without an author elem in the tei header.")
        else:
            print("\nGOOD!! All IPQs have an author element in the titleStatement.")

        self.assertEqual(bad_freetext_title, 0)


    #@unittest.skip
    def test_titleStmt_title(self):
        ipqs = self._fetch_data_paths()
        bad_freetext_title = 0
        missing_titles = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            title_t = root.find(f".//{t}titleStmt/{t}title")
            if title_t is None or (title_t.text is None or title_t.text == ''):
                bad_freetext_title += 1
                missing_titles.append(ipq)

        if bad_freetext_title > 0:
            print("\n¡¡BAD!! Author in titleStatment:",
                  str(bad_freetext_title), "of", str(len(ipqs)), "|",
                  str(bad_freetext_title/len(ipqs)),
                  "without a title elem in the tei header.")
        else:
            print("\nGOOD!! All IPQs have an title element in the titleStatement.")

        self.assertEqual(bad_freetext_title, 0)


    #@unittest.skip
    def test_bibl(self):
        ipqs = self._fetch_data_paths()
        bad_bibl = 0
        bad_bibls = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            bibl = root.find(f".//{t}sourceDesc/{t}bibl")
            if bibl is None or (len(bibl) == 0 and len(bibl.text) == 0):
                bad_bibl += 1
                bad_bibls.append(ipq)

        if bad_bibl > 0:
            print("\n¡¡BAD!! Missing or empty bibl elem in sourceDesc:",
                  str(bad_bibl), "of", str(len(ipqs)), "|",
                  str(bad_bibl/len(ipqs)))
        else:
            print("\nGOOD!! All IPQs have a bibl elem with something in it.")

        self.assertEqual(bad_bibl, 0)


    #@unittest.skip
    def test_listPerson(self):
        ipqs = self._fetch_data_paths()
        empty_list = 0
        empty_lists = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            listPerson = root.find(f".//{t}listPerson")
            if listPerson is None or len(listPerson) < 2:
                empty_list += 1
                empty_lists.append(ipq)

        if empty_list > 0:
            print("\n¡¡BAD!! too short person list",
                  str(empty_list), "of", str(len(ipqs)), "|",
                  str(empty_list/len(ipqs)))
        else:
            print("\nGOOD!! All IPQs have a person list with reasonable length.")

        self.assertEqual(empty_list, 0)


    #@unittest.skip
    def test_person_id(self):
        ipqs = self._fetch_data_paths()
        person_count = 0
        person_no_id = 0
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            persons = root.findall(f".//{t}person")
            for person in persons:
                person_count += 1
                idno = person.find(f"{t}idno")
                if idno is None:
                    person_no_id += 1
                else:
                    if idno.text.startswith("r-"):
                        person_no_id += 1
        print(f"\nPERSON ID TEST: {person_no_id} of {person_count} missing ID :: {person_no_id/person_count}")

    #@unittest.skip
    def test_person_gender(self):
        ipqs = self._fetch_data_paths()
        person_count = 0
        person_no_gen = 0
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            persons = root.findall(f".//{t}person")
            for person in persons:
                person_count += 1
                if "gender" in person.attrib:
                    if person.attrib['gender'] == "man" or person.attrib['gender'] == "woman":
                        pass
                    else:
                        person_no_gen += 1
                else:
                    person_no_gen += 1
        print(f"\nPERSON GENDER TEST: {person_no_gen} of {person_count} missing gender label :: {person_no_gen/person_count}")


    #@unittest.skip
    def test_correspDesc(self):
        ipqs = self._fetch_data_paths()
        empty_list = 0
        empty_lists = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            correspDesc = root.find(f".//{t}correspDesc")
            if correspDesc is None or len(correspDesc) < 2:
                empty_list += 1
                empty_lists.append(ipq)

        if empty_list > 0:
            print("\n¡¡BAD!! too short correspDesc",
                  str(empty_list), "of", str(len(ipqs)), "|",
                  str(empty_list/len(ipqs)))
        else:
            print("\nGOOD!! All IPQs have a correspDesc with reasonable length.")

        self.assertEqual(empty_list, 0)


    #@unittest.skip
    def test_questionStatus(self):
        ipqs = self._fetch_data_paths()
        isna = 0
        isnas = []
        isunk = 0
        isunks = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            status = root.find(f".//{t}correspAction[@type='questionStatus']")

            if status is None:
                isna += 1
                isnas.append(ipq)
            else:
                subt = status.attrib.get("subtype", None)
                if subt == "unknown":
                    isunk += 1
                    isunks.append(ipq)

        if isna > 0:
            print("\n¡¡Missing status:")
            print("  |~~ No staus elem",
                  str(isna), "of", len(ipqs), "|",
                  str(isna/len(ipqs)))
            print("  |~~ Unknown status",
                  str(isunk), "of", len(ipqs), "|",
                  str(isunk/len(ipqs)))
            print("  |~~ Known status",
                  str(len(ipqs)-(isunk+isna)), "of", len(ipqs), "|",
                  str((len(ipqs)-(isunk+isna)) / len(ipqs)))


    #@unittest.skip
    def test_correspContext(self):
        ipqs = self._fetch_data_paths()
        isna = 0
        isnas = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            contexts = root.findall(f".//{t}correspContext/{t}ref[@type='record']")

            if contexts is None or len(contexts) == 0:
                isna += 1
                isnas.append(ipq)
        if isna > 0:
            print("\n¡¡Missing protocol reference:")
            print("  |~~ No protocol reference",
                str(isna), "of", len(ipqs), "|",
                str(isna/len(ipqs)))


    #@unittest.skip
    def test_body_ipqContext(self):
        ipqs = self._fetch_data_paths()
        bad_context = 0
        bad_contexts = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            isna = False
            non_empty_p = False
            context = root.find(f".//{t}div[@type='ipqContext']")
            if context is None:
                isna = True
            else:
                for p in context:
                    if p.text is not None and len(p.text) > 0:
                        non_empty_p = True
            if isna == True or non_empty_p == False:
                bad_context += 0
                bad_contexts.append(ipq)
        if bad_context > 0:
            print("\n¡¡BAD!! Empty or missing ipqContext:",
                  str(bad_context), "of", str(len(ipqs)), "|",
                  str(bad_context/len(ipqs)))
        else:
            print("\nGOOD!! All IPQs have a non-emtpy ipqContext div.")

        self.assertEqual(bad_context, 0)


    #@unittest.skip
    def test_body_ipqQuestion(self):
        ipqs = self._fetch_data_paths()
        bad_context = 0
        bad_contexts = []

        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            isna = False
            non_empty_p = False
            context = root.find(f".//{t}div[@type='ipQuestion']")
            if context is None:
                isna = True
            else:
                for p in context:
                    if p.text is not None and len(p.text) > 0:
                        non_empty_p = True
            if isna == True or non_empty_p == False:
                bad_context += 1
                bad_contexts.append(ipq)
        if bad_context > 0:
            print("\n¡¡BAD!! Empty or missing ipqQuestion:",
                  str(bad_context), "of", str(len(ipqs)), "|",
                  str(bad_context/len(ipqs)))
        else:
            print("\nGOOD!! All IPQs have a non-emtpy ipQuestion div.")

        #self.assertEqual(bad_context, 0)


    ### ~~~~~~~ DEPRECIATED TESTS BELOW ~~~~~~~~~~~~ ###

    @unittest.skip
    def test_head(self):
        """
        depreciated -- old schema
        """
        ipqs = self._fetch_data_paths()
        bad_freetext = 0
        bad = []
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            head = root.find(f"{t}text/{t}front/{t}div/{t}head")
            if head.text == "xyz":
                bad_freetext += 1
                bad.append(ipq)

        if bad_freetext > 0:
            print("HEAD freetext:", str(bad_freetext), "of", str(len(ipqs)), "|", str(bad_freetext/len(ipqs)), "with generic freetext")
            print("HEAD freetext in", bad, "no bueno")

        self.assertEqual(bad_freetext, 0)


    @unittest.skip
    def test_minister_who(self):
        """
        depreciated -- old schema
        """
        ipqs = self._fetch_data_paths()
        bad_freetext = 0
        unknowns_n = 0
        unknowns = []
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            minister = root.find(f"{t}text/{t}front/{t}div/{t}minister")

            if minister.text == "minister freetext":
                bad_freetext += 1
            if minister.attrib['who'] == "unknown":
                unknowns_n += 1
                unknowns.append([ipq, minister.text])

        if bad_freetext > 0:
            print("MINISTER freetext:", str(bad_freetext), "of", str(len(ipqs)), "|", str(bad_freetext/len(ipqs)), "with generic freetext")
        if unknowns_n > 0:
            print("MINISTER unknowns:", str(unknowns_n), "of", str(len(ipqs)), "|", str(unknowns_n/len(ipqs)), "unmatched to person medatata")
            [print(_) for _ in unknowns]

        self.assertEqual(bad_freetext, 0)
        #self.assertEqual(unknowns_n, 0)

    @unittest.skip
    def test_topic(self):
        """
        depreciated -- old schema
        """
        ipqs = self._fetch_data_paths()
        bad_freetext = 0
        bad = []
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            topic = root.find(f"{t}text/{t}front/{t}div/{t}topic")
            if topic.text == "topic freetext":
                bad_freetext += 1
                bad.append(ipq)

        if bad_freetext > 0:
            print("TOPIC freetext:", str(bad_freetext), "of", str(len(ipqs)), "|", str(bad_freetext/len(ipqs)), "with generic freetext")
            print("TOPIC freetext in", bad, "no bueno")

        self.assertEqual(bad_freetext, 0)

    @unittest.skip
    def test_date(self):
        """
        depreciated -- old schema
        """
        ipqs = self._fetch_data_paths()
        bad_freetext = 0
        bad = []
        bad_when = []
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            date = root.find(f"{t}text/{t}front/{t}div/{t}docDate")
            if date.text == "date freetext":
                bad_freetext += 1
                bad.append(ipq)
            try:
                when = date.attrib["when"]
            except:
                bad_when.append([ipq, date.text])
            else:
                if when == "yyyy-mm-dd":
                    bad_when.append([ipq, date.text])

        if bad_freetext > 0:
            print("DATE freetext:", str(bad_freetext), "of", str(len(ipqs)), "|", str(bad_freetext/len(ipqs)), "with generic freetext")
            print("DATE freetext in", bad, "no bueno")
        if len(bad_when) > 0:
            print("DATE when attrib:", str(bad_when), "of", str(len(ipqs)), "|", str(bad_when/len(ipqs)), "with generic freetext")
            print("DATE when attrib in", bad_when, "no bueno")

        self.assertEqual(bad_freetext, 0)
        self.assertEqual(len(bad_when), 0)


    @unittest.skip
    def test_status(self):
        """
        depreciated -- old schema
        """
        ipqs = self._fetch_data_paths()
        bad_freetext = 0
        unknowns = []
        bad = []
        bad_when = []
        bad_prot = []
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            status = root.find(f"{t}text/{t}front/{t}div/{t}status")
            if status.text == "answered":
                bad_freetext += 1
                bad.append(ipq)
            Qstatus = status.attrib["status"]
            if Qstatus == 'unknown':
                unknowns.append(ipq)
            try:
                when = status.attrib["when"]
            except:
                if Qstatus == "answered":
                    bad_when.append([ipq, status.text])
            else:
                if when == "yyyy-mm-dd":
                    bad_when.append([ipq, status.text])
            try:
                prot = status.attrib["inProtocol"]
            except:
                if Qstatus == "answered":
                    bad_prot.append(ipq)
            else:
                if prot == "prot-abc123":
                    bad_prot.append(ipq)

        if bad_freetext > 0:
            print("STATUS freetext:", str(bad_freetext), "of", str(len(ipqs)), "|", str(bad_freetext/len(ipqs)), "with generic freetext")
            print("STATUS freetext in", bad, "no bueno")
        if len(unknowns) > 0:
            print("STATUS status attrib:", str(unknowns), "of", str(len(ipqs)), "|", str(unknowns/len(ipqs)), "with generic freetext")
            print("STATUS status attrib in", unknowns, "no bueno")
        if len(bad_when) > 0:
            print("STATUS when attrib:", str(bad_when), "of", str(len(ipqs)), "|", str(bad_when/len(ipqs)), "with generic freetext")
            print("STATUS when attrib in", bad_when, "no bueno")
        if len(bad_prot) > 0:
            print("STATUS protocol reference:", str(bad_prot), "of", str(len(ipqs)), "|", str(len(bad_prot)/len(ipqs)), "with generic freetext")
            print("STATUS protocol reference in", bad_prot, "no bueno")

        self.assertEqual(bad_freetext, 0)
        self.assertEqual(len(unknowns), 0)
        self.assertEqual(len(bad_when), 0)
        self.assertEqual(len(bad_prot), 0)



if __name__ == '__main__':
    unittest.main()

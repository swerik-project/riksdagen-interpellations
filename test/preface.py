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
    def test_head(self):
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


    #@unittest.skip
    def test_author_who(self):
        ipqs = self._fetch_data_paths()
        bad_freetext = 0
        unknowns_n = 0
        unknowns = []
        for ipq in ipqs:
            root, ns = parse_protocol(ipq, get_ns=True)
            t = ns['tei_ns']
            author = root.find(f"{t}text/{t}front/{t}div/{t}author")
            if author.text == "mp freetext":
                bad_freetext += 1
            if author.attrib['who'] == "unknown":
                unknowns_n += 1
                unknowns.append([ipq, author.text])

        if bad_freetext > 0:
            print("MP freetext:", str(bad_freetext), "of", str(len(ipqs)), "|", str(bad_freetext/len(ipqs)), "with generic freetext")
        if unknowns_n > 0:
            print("MP unknowns:", str(unknowns_n), "of", str(len(ipqs)), "|", str(unknowns_n/len(ipqs)), "unmatched to person medatata")
            [print(_) for _ in unknowns]

        self.assertEqual(bad_freetext, 0)
        #self.assertEqual(unknowns_n, 0)


    #@unittest.skip
    def test_minister_who(self):
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

    #@unittest.skip
    def test_topic(self):
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

    #@unittest.skip
    def test_date(self):
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


    #@unittest.skip
    def test_status(self):
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

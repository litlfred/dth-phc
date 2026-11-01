#!/usr/bin/env python3
"""Write processes/anc-registration-workflow-a.bpmn: Fig. 10 of the PHC handbook
(WHO ANC DAK Workflow A, Registration) rebuilt as BPMN 2.0 in the figure's own words.

The figure's labels come from who-iris vector-labels.json, PDF page 38. Layout: two
lanes as in the figure, fixed 120x120 tasks, right-angle flows. Re-run to regenerate.
"""
import sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1] if len(sys.argv) > 1 else "processes/anc-registration-workflow-a.bpmn"
POOL_X, LABEL_W = 0, 30
CLIENT = (0, 160)          # lane y, height
HW = (160, 710)
W = 1290

nodes = {}   # id -> (kind, name, cx, cy, w, h, parent)
def task(i, n, cx, cy, parent="P"): nodes[i] = ("task", n, cx, cy, 120, 120, parent)
def gw(i, n, cx, cy, parent="P"): nodes[i] = ("exclusiveGateway", n, cx, cy, 50, 50, parent)
def start(i, n, cx, cy, parent="P"): nodes[i] = ("startEvent", n, cx, cy, 36, 36, parent)
def end(i, n, cx, cy, parent="P"): nodes[i] = ("endEvent", n, cx, cy, 36, 36, parent)

start("Start", "Start", 80, 80)
task("T1", "1. Arrive at facility", 200, 80)
task("T2", "2. Rapid assessment and management (RAM)", 200, 250)
gw("G3", "3. Urgent referral necessary?", 330, 250)
end("EndC", "C. ANC referral", 440, 250)
task("T4", "4. Gather client details", 330, 420)
task("T5", "5. Search for client", 330, 600)
gw("G6", "6. Match found?", 450, 600)
SUB = ("Sub8", "8. Validate client details", 510, 480, 500, 240)   # id, name, x, y, w, h
start("S8Start", "", 545, 600, "Sub8")
task("T81", "8.1 Review socio-demographic data with client", 650, 600, "Sub8")
gw("G82", "8.2 Update needed?", 770, 600, "Sub8")
task("T83", "8.3 Update client details", 890, 600, "Sub8")
end("S8End", "", 985, 600, "Sub8")
task("T7", "7. Create client record", 650, 800)
task("T9", "9. Check-in client", 1110, 600)
end("EndB", "B. ANC contact", 1240, 600)

def box(i):
    if i == "Sub8": return SUB[2], SUB[3], SUB[4], SUB[5]
    k, n, cx, cy, w, h, p = nodes[i]
    return cx - w / 2, cy - h / 2, w, h
def R(i): x, y, w, h = box(i); return (x + w, y + h / 2)
def L(i): x, y, w, h = box(i); return (x, y + h / 2)
def T(i): x, y, w, h = box(i); return (x + w / 2, y)
def B(i): x, y, w, h = box(i); return (x + w / 2, y + h)

flows = [  # id, src, tgt, name, waypoints, parent
 ("F1", "Start", "T1", "", [R("Start"), L("T1")], "P"),
 ("F2", "T1", "T2", "", [B("T1"), T("T2")], "P"),
 ("F3", "T2", "G3", "", [R("T2"), L("G3")], "P"),
 ("F4", "G3", "EndC", "Yes", [R("G3"), L("EndC")], "P"),
 ("F5", "G3", "T4", "No", [B("G3"), T("T4")], "P"),
 ("F6", "T4", "T5", "", [B("T4"), T("T5")], "P"),
 ("F7", "T5", "G6", "", [R("T5"), L("G6")], "P"),
 ("F8", "G6", "Sub8", "Yes", [R("G6"), L("Sub8")], "P"),
 ("F9", "G6", "T7", "No", [B("G6"), (B("G6")[0], L("T7")[1]), L("T7")], "P"),
 ("F10", "Sub8", "T9", "", [R("Sub8"), L("T9")], "P"),
 ("F11", "T7", "T9", "", [R("T7"), (B("T9")[0], R("T7")[1]), B("T9")], "P"),
 ("F12", "T9", "EndB", "", [R("T9"), L("EndB")], "P"),
 ("F81", "S8Start", "T81", "", [R("S8Start"), L("T81")], "Sub8"),
 ("F82", "T81", "G82", "", [R("T81"), L("G82")], "Sub8"),
 ("F83", "G82", "T83", "Yes", [R("G82"), L("T83")], "Sub8"),
 ("F84", "T83", "S8End", "", [R("T83"), L("S8End")], "Sub8"),
 ("F85", "G82", "S8End", "No", [B("G82"), (B("G82")[0], 700), (B("S8End")[0], 700), B("S8End")], "Sub8"),
]

def outgoing(i): return [f for f in flows if f[1] == i]
def incoming(i): return [f for f in flows if f[2] == i]
def node_xml(i, ind):
    k, n, *_ = nodes[i]
    s = f'{ind}<bpmn:{k} id="{i}"' + (f' name="{esc(n)}"' if n else "") + ">\n"
    for f in incoming(i): s += f"{ind}  <bpmn:incoming>{f[0]}</bpmn:incoming>\n"
    for f in outgoing(i): s += f"{ind}  <bpmn:outgoing>{f[0]}</bpmn:outgoing>\n"
    return s + f"{ind}</bpmn:{k}>\n"
def flow_xml(f, ind):
    return f'{ind}<bpmn:sequenceFlow id="{f[0]}" sourceRef="{f[1]}" targetRef="{f[2]}"' + (f' name="{f[3]}"' if f[3] else "") + "/>\n"

client_nodes = ["Start", "T1"]
hw_nodes = [i for i, v in nodes.items() if v[6] == "P" and i not in client_nodes] + ["Sub8"]

x = []
x.append('<?xml version="1.0" encoding="UTF-8"?>\n')
x.append('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Definitions_Process_AncRegistrationWorkflowA" targetNamespace="https://litlfred.github.io/dth-phc/workflows" exporter="folio-assistant" exporterVersion="1">\n')
x.append('  <bpmn:resource id="pers:health-service-user" name="Client"/>\n')
x.append('  <bpmn:resource id="pers:health-worker" name="Health worker or Clerk"/>\n')
x.append('  <bpmn:collaboration id="Collaboration_AncRegistrationWorkflowA">\n    <bpmn:participant id="Participant_HealthFacility" name="Health facility" processRef="Process_AncRegistrationWorkflowA"/>\n  </bpmn:collaboration>\n')
x.append('  <bpmn:process id="Process_AncRegistrationWorkflowA" name="Workflow A: Registration business process" isExecutable="false">\n')
x.append('    <bpmn:documentation>Fig. 10 of WHO 9789240093362 (PDF page 38), rebuilt as BPMN in the figure\'s own words. Source: WHO (29), the WHO Digital adaptation kit for antenatal care (ANC.A). Notes and annotations for each activity: Fig. 11 (tbl:fig-11).</bpmn:documentation>\n')
x.append('    <bpmn:laneSet id="LaneSet_AncRegistrationWorkflowA">\n')
x.append('      <bpmn:lane id="Lane_Client" name="Client" partitionElementRef="pers:health-service-user">\n' + "".join(f"        <bpmn:flowNodeRef>{i}</bpmn:flowNodeRef>\n" for i in client_nodes) + "      </bpmn:lane>\n")
x.append('      <bpmn:lane id="Lane_HealthWorkerOrClerk" name="Health worker or Clerk" partitionElementRef="pers:health-worker">\n' + "".join(f"        <bpmn:flowNodeRef>{i}</bpmn:flowNodeRef>\n" for i in hw_nodes) + "      </bpmn:lane>\n")
x.append('    </bpmn:laneSet>\n')
for i, v in nodes.items():
    if v[6] == "P": x.append(node_xml(i, "    "))
x.append(f'    <bpmn:subProcess id="Sub8" name="{esc(SUB[1])}">\n')
for f in incoming("Sub8"): x.append(f"      <bpmn:incoming>{f[0]}</bpmn:incoming>\n")
for f in outgoing("Sub8"): x.append(f"      <bpmn:outgoing>{f[0]}</bpmn:outgoing>\n")
for i, v in nodes.items():
    if v[6] == "Sub8": x.append(node_xml(i, "      "))
for f in flows:
    if f[5] == "Sub8": x.append(flow_xml(f, "      "))
x.append('    </bpmn:subProcess>\n')
for f in flows:
    if f[5] == "P": x.append(flow_xml(f, "    "))
x.append('  </bpmn:process>\n')
x.append('  <bpmndi:BPMNDiagram id="Diagram_AncRegistrationWorkflowA">\n    <bpmndi:BPMNPlane id="Plane_AncRegistrationWorkflowA" bpmnElement="Collaboration_AncRegistrationWorkflowA">\n')
# Label boxes (x, y, w, h) kept clear of the flows: gateway names above the diamond.
LABELS = {
 "G3": (270, 166, 120, 50), "G6": (390, 540, 120, 30), "G82": (642, 666, 122, 36),
 "F5": (338, 300, 24, 16), "F9": (456, 650, 24, 16), "F85": (840, 702, 24, 16),
 "F4": (392, 228, 30, 16), "F8": (480, 580, 30, 16), "F83": (800, 580, 30, 16),
}
def lab(el):
    if el not in LABELS: return ""
    X, Y, w, h = LABELS[el]
    return f'<bpmndi:BPMNLabel><dc:Bounds x="{X:g}" y="{Y:g}" width="{w:g}" height="{h:g}"/></bpmndi:BPMNLabel>'
def shape(el, bx, extra=""):
    X, Y, w, h = bx
    return f'      <bpmndi:BPMNShape id="{el}_di" bpmnElement="{el}"{extra}><dc:Bounds x="{X:g}" y="{Y:g}" width="{w:g}" height="{h:g}"/>{lab(el)}</bpmndi:BPMNShape>\n'
x.append(shape("Participant_HealthFacility", (POOL_X, 0, W, HW[0] + HW[1]), ' isHorizontal="true"'))
x.append(shape("Lane_Client", (LABEL_W, CLIENT[0], W - LABEL_W, CLIENT[1]), ' isHorizontal="true"'))
x.append(shape("Lane_HealthWorkerOrClerk", (LABEL_W, HW[0], W - LABEL_W, HW[1]), ' isHorizontal="true"'))
for i in nodes:
    x.append(shape(i, box(i)))
x.append(shape("Sub8", box("Sub8"), ' isExpanded="true"'))
for f in flows:
    wp = "".join(f'<di:waypoint x="{p[0]:g}" y="{p[1]:g}"/>' for p in f[4])
    x.append(f'      <bpmndi:BPMNEdge id="{f[0]}_di" bpmnElement="{f[0]}">{wp}{lab(f[0])}</bpmndi:BPMNEdge>\n')
x.append('    </bpmndi:BPMNPlane>\n  </bpmndi:BPMNDiagram>\n</bpmn:definitions>\n')
open(OUT, "w").write("".join(x))
print("wrote", OUT)

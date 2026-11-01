Digital systems can go beyond simple data collection and aggregation by introducing additional 
layers of sophistication that are generally unavailable on paper. This includes the opportunity to 
enhance care provision with built-in decision-support logic. 
In PCPOSSs, embedded decision-support logic can help health 
workers follow appropriate clinical care pathways set out by 
WHO and national public health authorities’ guidelines and 
recommendations. The decision-support logic that can be 
integrated includes: 
•	 scheduling
•	 asking
•	 risk assessment for triage and/or referrals
•	 medical eligibility. 
These decision support mechanisms should be directed by 
clinical and evidence-based protocols that have been outlined 
by WHO or the national governing agency (e.g. the public 
health authority). 
This section describes the methods for documenting 
scheduling logic and other decision-support logic, which will 
be used to inform the back-end formulas in the PCPOSS. There 
are many ways to document and design decision-support logic. 
Decision-support logic in care pathways can be represented in 
many ways, including decision trees and/or decision-support 
tables. The methods outlined here are designed to be as simple 
as possible to use while still ensuring comprehensiveness. 
3.6.1 	 Document clinical care pathway decision-support logic
The health worker occupational group relevant to the target 
end-users dictates the clinical protocol to be embedded in 
a PCPOSS. For example, a risk-profiling decision-support 
logic can be used for the identification and prioritization of 
health service users who are at greater risk of adverse health 
outcomes. The identification of a high-risk pregnancy, for 
example, could provide risk-profiling decision support for a 
nurse/midwife doing triage, but could also give risk-profiling 
decision support to a community health worker for the 
purposes of referral. 
The clinical protocols used in the PCPOSS should follow WHO 
and/or national public health authority recommendations. 
Reference decision support logic
Depending on the health area targeted, there may 
already be decision-support logics and algorithms 
documented, in accordance with WHO guidelines. WHO’s 
Digital adaptation kits (DAKs) provide a starting point 
for decision support logic and algorithms to support 
guidelines-based service delivery. For example, WHO’s 
DAK for family planning outlines the decision support 
tables for family planning counselling and medical 
eligibility (30). Adaptation of WHO’s DAKs may require 
changes in thresholds or triggers in a logic statement and 
additional decision support logic formulas depending on 
national policies and context.
Safe decision support systems
If there is no clinical care pathway decision-support logic that is in line with evidence-based global or national normative 
guidelines, reconsider the inclusion of this decision-support logic in the system. Changes to the decision-support logic 
should be considered carefully and any new additions should be agreed upon by clinical experts. Inappropriate or 
inaccurate decision logic can put health service user’s safety and wellbeing at risk. 
TIP
WARNING
Decision-support logic matrix
A matrix of “decision-support logic” provides an inventory 
(i.e. listing) of all the decision-support logics made in clinical 
care pathways. Fig. 13 offers an example from the DAK for HIV, 
and Annex 10 offers a guide for the decision-support logic 
matrix, with brief explanations of the components needed to 
complete it. Note that the decision-support logics identified in 
the matrix are only intended to provide an overview of what 
is detailed further as decision trees and/or decision-support 
tables. 
Decision trees
A decision tree is a visual representation of the logic in 
the PCPOSS that directs the series of decisions applied in 
care pathways. Visualizing the relationships, linkages and 
dependencies between each decision helps to determine what 
the health worker needs to do next, or which screen needs 
to be displayed on the PCPOSS after a given set of inputs. 
Decision trees may be particularly useful for decision points 
that consist of multiple inputs and outputs.
Clinical protocols and algorithms depicted with decision trees 
can be based on a selected health worker occupational group, 
but note that in some settings, and depending on task-shifting 
policies, one decision logic could involve more than one health 
worker occupational group. 
WHO’s DAK for ANC provides examples of decision trees 
to supplement the use of decision-support tables (29). 
For example, Fig. 14 depicts a decision tree for antenatal 
registration for HIV testing and counselling. Each box 
represents one decision, which is represented by an algorithm 
or a series of algorithms. If that decision’s output(s) become 
another decision’s input(s), these two decisions are linked. The 
arrows show the sequence of decisions in a care pathway.
Decision trees are different from workflow diagrams. In the 
workflows mapped in section 3.3, activities would indicate 
whether a decision needs to be made. The proceeding tasks 
or activity following the outcomes of decisions might be the 
same, but the content associated with the tasks or activity 
might differ. Decision trees fill this gap. Each box in a decision 
tree will need to be further detailed so that engineers can 
programme the decision-support logic into software.

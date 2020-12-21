from treelib import Node, Tree
from resource import Resource

class Testing_Decision_Tree:

    def __init__(self):
        # read from json and auto populate a tree
        self.tree = Tree()
        self.tree.create_node(tag="Will You Test", identifier=1,
                              data=Resource(explanation="This is a major choice you have to make. Will you provide "
                                                        "in-school testing? There are pros and cons to this option. "
                                                        "By providing in-school testing, you will increase access to "
                                                        "tests for the families in your district, and you will decrease"
                                                        " the likelihood of transmission within your school building. "
                                                        "You will also be able to better control your knowledge of "
                                                        "infection levels in your school.<br>However, when you test, "
                                                        "you WILL find cases. You will have to provide careful "
                                                        "messaging to your staff, students, and parents regarding "
                                                        "the meaning of test results. Remember, a negative test simply "
                                                        "means that there was not sufficient virus to be detected at "
                                                        "that time – it is no guarantee of safety, nor is it a free"
                                                        " pass to relax other important controls (such as masks and "
                                                        "distancing).<br>You will also need to develop policies around "
                                                        "testing. Who will be tested, where, when, and how? How will "
                                                        "test results be reported? What test will be used?<br>There is no"
                                                        " single testing protocol that will work for every school. The "
                                                        "choices you make must be based on your circumstances, "
                                                        "including financial and social constraints. Below, we present "
                                                        "some considerations related to these choices, as well as some "
                                                        "examples.", file_list=["Consent document",
                                                                                "Guidance for Cleaning and Disinfecting _ CDC.pdf"]))  # root node

        self.tree.create_node("Will you require testing", 2, parent=1,
                              data=Resource(explanation="The CDC has ruled that employers may require COVID-19 tests of"
                                                        " their employees, but the legality of mandatory testing of "
                                                        "students has not been firmly established. Therefore, the "
                                                        "decision to require testing of students will depend in part "
                                                        "on the opinions and support of the parents. ",
                                            file_list=["Testing population description"]))
        self.tree.create_node("Who will you be testing", 3, parent=1,
                              data=Resource(explanation="CDC has established that you may not ethically test students "
                                                        "without parental consent. Therefore, you will need a consent "
                                                        "document, signed by parents, that stipulates what testing will "
                                                        "be done, how the results will be reported, and what will be "
                                                        "done to protect privacy and safety. Examples of these "
                                                        "documents are available here", file_list=["HR/union agreement"]))
        self.tree.create_node("Where will testing happen", 4, parent=1,
                              data=Resource(explanation="You can choose to collect test samples at home or at school."))
        self.tree.create_node("How often will you test", 5, parent=1,
                              data=Resource(explanation="Testing frequency can vary based on practicalities, including"
                                                        " availability of tests. Weekly testing would be the minimum "
                                                        "for reliable detection of infectious individuals; daily or "
                                                        "biweekly would be preferred.<br>It is possible to use varied "
                                                        "testing frequency effectively. For instance, high-risk "
                                                        "individuals (such as those in team sports) may require more "
                                                        "frequent testing. If test supplies are limited, more frequent "
                                                        "testing of teachers, especially those in contact with a "
                                                        "larger number of students, could be used"))
        self.tree.create_node("How to share results", 6, parent=1,
                              data=Resource(explanation="When you test, the results of the tests will need to be "
                                                        "reported. At the very least, parents will need to be informed "
                                                        "of their child’s results and staff will need to be informed of "
                                                        "their own results. You may need to check with your local Public"
                                                        " Health department to determine your responsibility for "
                                                        "sharing results with them."))
        self.tree.create_node("Which test will you use", 7, parent=1,
                              data=Resource(explanation="What test is available to you? A summary of tests and their "
                                                        "uses is available here. The test you select will determine "
                                                        "the supplies you need, the speed at which results come, and "
                                                        "the cost."))

        self.tree.create_node("Mandatory", 8, parent=2,
                              data=Resource(explanation="It would be assumed that all in-person individuals will be "
                                                        "required to test. You should ensure a sufficient supply of "
                                                        "tests.<br>Will you also provide testing for those who remain "
                                                        "remote? If so, you will need to establish a process for "
                                                        "collecting test samples from those not in the building "
                                                        "regularly.<br>An enforcement mechanism must be in place. For "
                                                        "students, this could be as simple as an attendance list "
                                                        "updated each week to flag any student who has missed a test."
                                                        " For staff, a roster may be the easiest mechanism.",
                                            file_list=["Enforcement policy", "Collection schedule", "HR/union agreement"]))
        self.tree.create_node("Voluntary", 9, parent=2,
                              data=Resource(explanation="You will need to determine the expected number of people "
                                                        "wanting access to testing. This could be found through a "
                                                        "survey or through return of consent forms. Again, you will "
                                                        "need to ensure a sufficient supply of tests.<br>Will testing be "
                                                        "on demand, or will it be scheduled? If on demand, you may want"
                                                        " to establish a system for individuals to self-schedule test "
                                                        "times; otherwise, testing locations may be overwhelmed at "
                                                        "certain times of day.  If scheduled, you will need a procedure"
                                                        " to avoid collecting samples from students whose parents have "
                                                        "not consented. Again, a simple roster or list will be "
                                                        "sufficient. You will also need to be careful about social "
                                                        "pressure (either for or against testing) being used to support"
                                                        " bullying.<br>Will testing be for symptomatic individuals only, "
                                                        "or will asymptomatic individuals be allowed testing? Remember"
                                                        " that younger people are unlikely to develop symptoms but do "
                                                        "appear to be infectious. In addition, asymptomatic adults are"
                                                        " just as infectious as symptomatic adults. We do not advise "
                                                        "limiting testing to symptomatic individuals."))
        self.tree.create_node("All", 10, parent=8, data=Resource())
        self.tree.create_node("In-person only", 11, parent=8, data=Resource())

        self.tree.create_node("Expected number", 12, parent=9, data=Resource())

        self.tree.create_node("All (teachers, staff, and students)", 13, parent=3,
                              data=Resource(explanation="This is recommended."))
        self.tree.create_node("Adults only", 14, parent=3,
                              data=Resource(explanation="Testing the teachers and staff only allows you to avoid the "
                                                        "process of obtaining consent from and communicating test "
                                                        "results to parents. However, children are known to be "
                                                        "infectious even if not symptomatic, and it is possible for a "
                                                        "large outbreak to develop among students before it becomes "
                                                        "apparent in the teachers and staff."))
        self.tree.create_node("Random sample", 15, parent=3,
                              data=Resource(explanation="If testing is limited, it is possible to use a sampling "
                                                        "technique. This could be performed by selecting a cohort of "
                                                        "individuals to be tested regularly, but that will limit the "
                                                        "effectiveness of testing. A better option is to select a "
                                                        "different sample of the population each week. This could be "
                                                        "done by selecting from a list of eligible individuals each "
                                                        "week, but it would be better to schedule each eligible person "
                                                        "to testing days at the beginning of the quarter.<br>If using "
                                                        "this method, you may want to have excess tests available for "
                                                        "the contacts of any positive individuals, as well as any "
                                                        "symptomatic individuals."))
        self.tree.create_node("Only high-risk inidividuals", 16, parent=3,
                              data=Resource(explanation="With very limited testing, it is possible to limit yourself to"
                                                        " those most likely to transmit within school. This would "
                                                        "include any groups that have close contact (such as sports "
                                                        "teams), who may have to be around unmasked students (such as"
                                                        " speech pathologists or lunchroom workers), or those who "
                                                        "participate in aerosol-generating activities (such as choir "
                                                        "members)."))

        self.tree.create_node("At home", 17, parent=4,
                              data=Resource(file_list=["Home collection instructions", "Chain of custody agreement",
                                                       "Sample return protocol", "Sample return drop point"]
        ))
        self.tree.create_node("In person (at school)", 18, parent=4,
                              data=Resource(explanation="When during the day and week will testing happen? Where will students "
                                            "and teachers be tested?",
                                            file_list=["Ventilation plan", "Signs for sample collection",
                                                       "Cleaning protocol"]))
        self.tree.create_node("Collection kits", 19, parent=17,
                              data=Resource(explanation="A collection kit should contain everything needed to collect "
                                                        "a sample, including clear instructions (example instructions "
                                                        "for nasal swab here, saliva sample here).<br>You can choose to "
                                                        "make collection kits that contain all testing supplies for a"
                                                        " quarter or a semester, or you can provide single-use testing "
                                                        "kits. If the former, you should provide extras in case of "
                                                        "mistakes. You should also post the instructions online, in "
                                                        "case the instructions are lost, and you should have extra "
                                                        "supplies to replace lost kits.<br>You will need to assemble the "
                                                        "collection kits, especially if you are providing a quarterly "
                                                        "supply. Zip-top bags are useful for this. Assembly can easily "
                                                        "be done by volunteers or using an assembly line process, just "
                                                        "make sure that the assembly team is distancing during the "
                                                        "process.<br>Ensuring a sufficient supply of kits requires "
                                                        "estimating the number needing a test, the frequency of "
                                                        "testing, and the duration of testing. The spreadsheet here "
                                                        "can help you calculate the number of supplies needed.",
                                            file_list=["Collection supply kits or inventory"]))
        self.tree.create_node("How will you maintain chain of custody", 20, parent=17,
                              data=Resource(explanation="Chain of custody means the process of ensuring that the sample "
                                                        "being tested came from the person whose information is"
                                                        " attached to the sample. It is difficult to establish with "
                                                        "home testing. We would recommend that an agreement to ensure"
                                                        " the test sample is appropriately collected and labeled be "
                                                        "signed by an adult (either staff member or parent); while "
                                                        "this does not guarantee chain of custody, it discourages"
                                                        " misbehavior"))
        self.tree.create_node("How will samples be returned", 21, parent=17,
                              data=Resource(explanation="The simplest way to return samples would be to have a secure "
                                                        "drop point (either box or rack) at entrances. This should be "
                                                        "an observed process, especially if testing is mandatory. "
                                                        "Handling of samples is not advised, as it could unnecessarily "
                                                        "expose the person collecting the samples."))
        self.tree.create_node("Weekly supply", 22, parent=19,
                              data=Resource(file_list=["Test supply chain/laboratory contracts"]))
        self.tree.create_node("Quarterly supply", 23, parent=19,
                              data=Resource(file_list=["Test supply chain/laboratory contracts"]))

        self.tree.create_node("Timing", 24, parent=18, data=Resource())
        self.tree.create_node("Where", 25, parent=18, data=Resource(file_list=["Test/collection site staffing plan"]))
        self.tree.create_node("In the classroom", 26, parent=25,
                              data=Resource(explanation="The testing personnel should have a schedule to move to each "
                                                        "location. They will need a cart of some kind to carry the "
                                                        "collection materials and the collected samples. The cart "
                                                        "should also contain instruction signs to assist students in "
                                                        "sample collection, cleaning equipment for spills, and "
                                                        "biohazard bins or bags for collecting waste.<br>Be aware that "
                                                        "some teachers may be uncomfortable remaining in the room while"
                                                        " students provide test samples. The testing personnel should "
                                                        "be sufficient in number to supervise the class during the "
                                                        "testing process if needed."))
        self.tree.create_node("In a testing center", 27, parent=25,
                              data=Resource(explanation="The testing center must be a central location with a clear "
                                                        "traffic flow pattern to avoid mixing at entrance and exit. "
                                                        "Signs should make the flow pattern clear.<br>Depending on the "
                                                        "number to be tested and the time required, it is possible "
                                                        "that a testing center could be made available only one day a "
                                                        "week, which would ensure availability of that space for other"
                                                        " activities the rest of the week. If that is the case, "
                                                        "thorough cleaning should be performed before and after the "
                                                        "testing center is run."))
        self.tree.create_node("Sample movement", 28, parent=26, data=Resource())
        self.tree.create_node("Traffic flow", 29, parent=27, data=Resource(file_list=["Contact tracing flow chart"]))

        self.tree.create_node("With Parents/staff", 30, parent=6,
                              data=Resource(explanation="You cannot provide medical test results directly to minors, "
                                                        "so student results will need to be shared with parents. "
                                                        "However, because medical test results are protected "
                                                        "information, the means by which you share results must be "
                                                        "HIPAA-compliant. You should work with your test provider to "
                                                        "determine the best method.<br>When deciding on a communications"
                                                        " strategy, remember the need for accessibility. Online or "
                                                        "smartphone systems will not be available to those with "
                                                        "limited internet access. Often, multiple contact methods"
                                                        " can be combined, with parents choosing their preferred "
                                                        "method.",
                                            file_list=["Parent communication plan"]))
        self.tree.create_node("With Public Health", 31, parent=6,
                              data=Resource(explanation="If you are working with a medical laboratory, they will be "
                                                        "reporting test results directly to Public Health. It would be "
                                                        "good to discuss this process with them, so you are aware of"
                                                        " their procedures.<br>If you are using in-house rapid tests, "
                                                        "you may be responsible for reporting to Public Health. It is "
                                                        "best to contact your local Public Health department as you "
                                                        "are making your plans so you know the information you must "
                                                        "report, the method of reporting, and your legal "
                                                        "obligations.",
                                            file_list=["Public health reporting and coordination process"]))
        self.tree.create_node("With the community", 32, parent=6,
                              data=Resource(explanation="Your school community, and the community at large, "
                                                        "will want to know about cases within your school. How you "
                                                        "inform them can vary, but it must, at minimum, preserve the "
                                                        "privacy of any detected cases. That means that information "
                                                        "should be shared publicly only in such a way that the "
                                                        "identity of a case cannot be deduced. In a small school, "
                                                        "or with specialty teachers and coaches, that can be extremely "
                                                        "difficult. Aggregation is the best technique to use to "
                                                        "preserve privacy. This refers to reporting results only among "
                                                        "groups; for instance, you might report only the grade of a "
                                                        "student testing positive.",
                                            file_list=["Community communication plan"]))
        self.tree.create_node("With close contacts", 33, parent=6,
                              data=Resource(explanation="When a positive case has been found, Public Health will often"
                                                        " perform contact tracing, in which any close contacts are "
                                                        "informed 1) that they may have been exposed, 2) the day of "
                                                        "the exposure, and 3) the regulations regarding quarantine. "
                                                        "You should contact your local Public Health district to "
                                                        "determine if you can help with their contact tracing "
                                                        "process.<br>If your local Public Health department is not "
                                                        "currently performing contact tracing, it will fall to you "
                                                        "to determine if anyone within your school should be notified"
                                                        " of a potential exposure. The CDC definition of a close "
                                                        "contact is someone who has spent at least 15 minutes"
                                                        " (cumulative) within 6 feet of the infected individual"
                                                        " between 48 hours prior to their diagnosis or the start"
                                                        " of their symptoms and the start of their isolation. "
                                                        "Among small children, that may be impossible to determine;"
                                                        " quarantine of an entire class would be a strong precaution"
                                                        " but might be justified.<br>One tension between preserving "
                                                        "privacy and protecting health will arise with those who "
                                                        "are able to identify the potential case. Teachers will likely"
                                                        " fall into this category – they will recognize the student "
                                                        "who is missing from their class. However, it is good practice"
                                                        " to inform teachers that a student of theirs has tested "
                                                        "positive, as they may need to take extra precautions to "
                                                        "protect their family members."))

        self.tree.create_node("What sample type will you need to collect", 34, parent=7,
                              data=Resource(explanation="You will likely need either saliva or a nasal swab. "
                                                        "Both can be self-collected, although younger students may "
                                                        "struggle with self-collection. A nasal swab can also be "
                                                        "collected by a health professional.",
                                            file_list=["Nasal bleed protocol (nasal swab only)",
                                                       "Saliva exemption policy (saliva only)"]))
        self.tree.create_node("How fast will you get results", 35, parent=7,
                              data=Resource(explanation="A test with a long delay may not be of use. If test reporting "
                                                        "delays will be longer than a few days, you may want to "
                                                        "reconsider your testing program."))
        self.tree.create_node("cost", 36, parent=7,
                              data=Resource(explanation="Remember that the cost of testing includes supplies, "
                                                        "personnel time, the laboratory process, and the reporting "
                                                        "mechanism. Ensure that you are sufficiently funded to cover "
                                                        "all aspects of the cost before deciding how many tests you "
                                                        "are able to perform.",
                                            file_list=["Financial plan"]))

if __name__ == "__main__":
    testing_decision_tree = Testing_Decision_Tree()
    testing_decision_tree.tree.show()

    # get node given id
    current = testing_decision_tree.tree.get_node(25)
    print("current:", vars(current.data))

    # check if it's the end
    print("is the end:", current.is_leaf())

    # list all the options
    options_pointers= current.fpointer
    print(testing_decision_tree.tree.children(25))

    # going back to last step
    print(testing_decision_tree.tree.children(current.bpointer))

    print(testing_decision_tree.tree.root)

    # test when submit find it's path
    print("\nstart traversing...")
    for node in testing_decision_tree.tree.rsearch(nid=25):
        print(node)
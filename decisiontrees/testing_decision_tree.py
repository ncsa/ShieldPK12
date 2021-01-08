from treelib import Tree

from resource import Resource


class Testing_Decision_Tree:

    def __init__(self):
        # read from json and auto populate a tree
        self.tree = Tree()

        self.tree.create_node(
            identifier="1",
            tag="Will You Test",
            data=Resource(
                question_type="single",
                explanation="This is a major choice you have to make. Will you provide in-school testing? There are "
                            "pros and cons to this option. By providing in-school testing, you will increase access "
                            "to tests for the families in your district, and you will decrease the likelihood of "
                            "transmission within your school building. You will also be able to better control your "
                            "knowledge of infection levels in your school."
                            "<br>"
                            "However, when you test, you WILL find cases. You will have to provide careful messaging "
                            "to your staff, students, and parents regarding the meaning of test results. Remember, a "
                            "negative test simply means that there was not sufficient virus to be detected at that "
                            "time – it is no guarantee of safety, nor is it a free pass to relax other important "
                            "controls (such as masks and distancing). "
                            "<br>"
                            "You will also need to develop policies around testing. Who will be tested, where, when, "
                            "and how? How will test results be reported? What test will be used? "
                            "<br>"
                            "There is no single testing protocol that will work for every school. The choices you "
                            "make must be based on your circumstances, including financial and social constraints. "
                            "Below, we present some considerations related to these choices, as well as some examples.",
                file_list=[]))  # root node

        self.tree.create_node(
            identifier="1a",
            tag="Yes",
            parent="1",
            data=Resource(
                question_type="multiple",
                explanation="Follow the remaining questions below to develop your testing protocol.",
                file_list=[]))

        self.tree.create_node(
            identifier="1b",
            tag="No",
            parent="1",
            data=Resource(
                explanation="You should have a protocol in place as to how external test results would be reported. "
                            "The process for reporting isolation and quarantine orders could be as simple as calling "
                            "the school office. We recommend providing the person(s) fielding those calls be provided "
                            "with basic information about how students in isolation and quarantine will be supported "
                            "(such as the example here). "
                            "<br>"
                            "The school should also have an established format for collecting information (the number "
                            "of days the person will be out, how they can be reached during that time, and, in the "
                            "case of an infected person, the date of the positive test). Contact tracing within the "
                            "school should happen for any person diagnosed with COVID-19 that was in the school "
                            "building for 48 hours prior to the positive test. See the contact tracing flow charts "
                            "(here) for more detail. "
                            "<br>"
                            "When a positive case has been found, Public Health will often perform contact tracing, "
                            "in which any close contacts are informed 1) that they may have been exposed, 2) the day "
                            "of the exposure, and 3) the regulations regarding quarantine. You should contact your "
                            "local Public Health district to determine if you can help with their contact tracing"
                            " process. If your local Public Health department is not currently performing contact "
                            "tracing, it will fall to you to determine if anyone within your school should be "
                            "notified of a potential exposure. The CDC definition of a close contact is someone "
                            "who has spent at least 15 minutes (cumulative) within 6 feet of the infected individual "
                            "between 48 hours prior to their diagnosis or the start of their symptoms and the start "
                            "of their isolation. Among small children, that may be impossible to determine; "
                            "quarantine of an entire class would be a strong precaution but might be justified."
                            "<br>"
                            "One tension between preserving privacy and protecting health will arise with those who "
                            "are able to identify the potential case. Teachers will likely fall into this category – "
                            "they will recognize the student who is missing from their class. However, it is good "
                            "practice to inform teachers that a student of theirs has tested positive, as they may "
                            "need to take extra precautions to protect their family members."
                            "<br>"
                            "Your school community, and the community at large, will want to know about cases within "
                            "your school. How you inform them can vary, but it must, at minimum, preserve the privacy "
                            "of any detected cases. That means that information should be shared publicly only in "
                            "such a way that the identity of a case cannot be deduced. In a small school, or with "
                            "specialty teachers and coaches, that can be extremely difficult. Aggregation is the "
                            "best technique to use to preserve privacy. This refers to reporting results only among "
                            "groups; for instance, you might report only the grade of a student testing positive.",
                file_list=[]))

        self.tree.create_node(
            identifier="2",
            tag="Who will you be testing",
            parent="1a",
            data=Resource(
                question_type="single",
                explanation="CDC has established that you may not ethically test students without parental consent. "
                            "Therefore, you will need a consent document, signed by parents, that stipulates what "
                            "testing will be done, how the results will be reported, and what will be done to protect "
                            "privacy and safety. Examples of these documents are available here",
                file_list=[]))

        self.tree.create_node(
            identifier="2a",
            tag="All (teachers, staff, and students)",
            parent="2",
            data=Resource(
                explanation="This is recommended",
                file_list=[]))

        self.tree.create_node(
            identifier="2b",
            tag="Adults only",
            parent="2",
            data=Resource(
                explanation="Testing the teachers and staff only allows you to avoid the process of obtaining consent"
                            " from and communicating test results to parents. However, children are known to be"
                            " infectious even if not symptomatic, and it is possible for a large outbreak to develop "
                            "among students before it becomes apparent in the teachers and staff."))

        self.tree.create_node(
            identifier="2c",
            tag="Sample",
            parent="2",
            data=Resource(
                explanation="If testing is limited, it is possible to use a sampling technique. This could be "
                            "performed by selecting a cohort of individuals to be tested regularly, but that will "
                            "limit the effectiveness of testing. A better option is to select a different sample of "
                            "the population each week. This could be done by selecting from a list of eligible "
                            "individuals each week, but it would be better to schedule each eligible person to "
                            "testing days at the beginning of the quarter."
                            "<br>"
                            "If using this method, you may want to have excess tests available for the contacts of "
                            "any positive individuals, as well as any symptomatic individuals"))

        self.tree.create_node(
            identifier="2d",
            tag="Only high-risk individuals",
            parent="2",
            data=Resource(
                explanation="With very limited testing, it is possible to limit yourself to those most likely to "
                            "transmit within school. This would include any groups that have close contact "
                            "(such as sports teams), who may have to be around unmasked students (such as speech "
                            "pathologists or lunchroom workers), or those who participate in aerosol-generating "
                            "activities (such as choir members)."))

        self.tree.create_node(
            tag="Will you require testing",
            identifier="3",
            parent="1a",
            data=Resource(
                question_type="single",
                explanation="The CDC has ruled that employers may require COVID-19 tests of their employees, but the "
                            "legality of mandatory testing of students has not been firmly established. Therefore, "
                            "the decision to require testing of students will depend in part on the opinions "
                            "and support of the parents.",
                file_list=[]))

        self.tree.create_node(
            tag="Mandatory",
            identifier="3a",
            parent="3",
            data=Resource(
                question_type="single",
                explanation="It would be assumed that all in-person individuals will be required to test. "
                            "You should ensure a sufficient supply of tests."
                            "<br>"
                            "Will you also provide testing for those who remain remote? If so, you will "
                            "need to establish a process for collecting test samples from those not in the "
                            "building regularly."
                            "<br>"
                            "An enforcement mechanism must be in place. For students, this could be as "
                            "simple as an attendance list updated each week to flag any student who has "
                            "missed a test. For staff, a roster may be the easiest mechanism. ",
                file_list=[]))

        self.tree.create_node(
            tag="Voluntary",
            identifier="3b",
            parent="3",
            data=Resource(
                question_type="single",
                explanation="You will need to determine the expected number of people wanting access to testing. "
                            "This could be found through a survey or through return of consent forms. Again, you will "
                            "need to ensure a sufficient supply of tests."
                            "<br>"
                            "Will testing be on demand, or will it be scheduled? If on demand, you may want to "
                            "establish a system for individuals to self-schedule test times; otherwise, testing "
                            "locations may be overwhelmed at certain times of day.  If scheduled, you will need a "
                            "procedure to avoid collecting samples from students whose parents have not consented. "
                            "Again, a simple roster or list will be sufficient. You will also need to be careful "
                            "about social pressure (either for or against testing) being used to support bullying."
                            "<br>"
                            "Will testing be for symptomatic individuals only, or will asymptomatic individuals "
                            "be allowed testing? Remember that younger people are unlikely to develop symptoms but "
                            "do appear to be infectious. In addition, asymptomatic adults are just as infectious as "
                            "symptomatic adults. We do not advise limiting testing to symptomatic individuals.",
                file_list=[]))

        self.tree.create_node(
            tag="Where will testing happen",
            identifier="4",
            parent="1a",
            data=Resource(
                question_type="single",
                explanation="You can choose to collect test samples at home or at school."))

        self.tree.create_node(
            tag="At home",
            identifier="4a",
            parent="4",
            data=Resource(
                question_type="multiple"
            ))

        self.tree.create_node(
            tag="Collection kits",
            identifier="4a-i",
            parent="4a",
            data=Resource(
                question_type="single",
                explanation="A collection kit should contain everything needed to collect a sample, including clear "
                            "instructions (example instructions for nasal swab here, saliva sample here)."
                            "<br>"
                            "You can choose to make collection kits that contain all testing supplies for a quarter "
                            "or a semester, or you can provide single-use testing kits. If the former, you should"
                            " provide extras in case of mistakes. You should also post the instructions online, in "
                            "case the instructions are lost, and you should have extra supplies to replace lost "
                            "kits."
                            "<br>"
                            "You will need to assemble the collection kits, especially if you are providing a "
                            "quarterly supply. Zip-top bags are useful for this. Assembly can easily be done by "
                            "volunteers or using an assembly line process, just make sure that the assembly team is "
                            "distancing during the process."
                            "<br>"
                            "Ensuring a sufficient supply of kits requires estimating the number needing a test, "
                            "the frequency of testing, and the duration of testing. The spreadsheet here can help "
                            "you calculate the number of supplies needed.",
                file_list=[]))

        self.tree.create_node(
            tag="How will you maintain chain of custody",
            identifier="4a-ii",
            parent="4a",
            data=Resource(
                explanation="Chain of custody means the process of ensuring that the sample being tested came from "
                            "the person whose information is attached to the sample. It is difficult to establish "
                            "with home testing. We would recommend that an agreement to ensure the test sample is "
                            "appropriately collected and labeled be signed by an adult (either staff member or "
                            "parent); while this does not guarantee chain of custody, it discourages misbehavior."
                            "<br>"
                            "How might chain of custody be broken? Be on the lookout for:"
                            "<li>Using a “clean” sample to avoid isolation</li>"
                            "<li>Using a sample from another family</li>"
                            "<li>member to expand testing access within the family</li>"
                            "<li>Mistakes, such as siblings putting samples in each other’s labeled tubes</li>",
                file_list=[]))

        self.tree.create_node(
            tag="How will samples be returned",
            identifier="4a-iii",
            parent="4a",
            data=Resource(
                explanation="The simplest way to return samples would be to have a secure drop point (either box or "
                            "rack) at entrances. This should be an observed process, especially if testing is "
                            "mandatory. Handling of samples is not advised, as it could unnecessarily expose the "
                            "person collecting the samples.")
            )

        self.tree.create_node(
            tag="In person",
            identifier="4b",
            parent="4",
            data=Resource(
                question_type="multiple"
            )
        )

        self.tree.create_node(
            tag="When during the day and week will testing happen",
            identifier="4b-i",
            parent="4b",
            data=Resource(
                explanation="It is unlikely that the entire school will test at the same time. Classes should be "
                            "scheduled for testing at a regular time, so that it can become part of classroom routine "
                            "and to avoid confusion. However, that means you will need a procedure for those who are "
                            "not present on their scheduled testing day."
                            "<br>"
                            "If using saliva tests, it is necessary to schedule sample collection around eating times, "
                            "to avoid interference caused by food residue – it is recommended that people not eat or "
                            "drink for an hour before saliva collection. For elementary, this would have to be "
                            "between breakfast/arrival and snack time, between snack time and lunch, or after lunch."))

        self.tree.create_node(
            tag="Where will students and teachers be tested",
            identifier="4b-ii",
            parent="4b",
            data=Resource(
                question_type="multiple",
                explanation="Sample collection could happen in the classroom or in a centralized testing center."
                            "<br>"
                            "One consideration in making this choice is ventilation. While saliva sampling does not "
                            "necessarily produce aerosols, the potential is there, especially with smaller children "
                            "for whom the distinction between drooling and spitting is difficult. If classrooms have "
                            "poor ventilation, a centralized location (such as a gymnasium) may be preferred. If a "
                            "central location with good ventilation is not available, classroom collection may be "
                            "preferred."
                            "<br>"
                            "The other main consideration is time. Especially with younger children, movement to and "
                            "from a central testing location could require a fair amount of class time."))

        self.tree.create_node(
            tag="In the classroom",
            identifier="4b-ii-1",
            parent="4b-ii",
            data=Resource(
                explanation="The testing personnel should have a schedule to move to each location. They will need a "
                            "cart of some kind to carry the collection materials and the collected samples. The cart "
                            "should also contain instruction signs to assist students in sample collection, cleaning "
                            "equipment for spills, and biohazard bins or bags for collecting waste."
                            "<br>"
                            "Be aware that some teachers may be uncomfortable remaining in the room while students "
                            "provide test samples. The testing personnel should be sufficient in number to supervise "
                            "the class during the testing process if needed."))

        self.tree.create_node(
            tag="In a testing center",
            identifier="4b-ii-2",
            parent="4b-ii",
            data=Resource(
                explanation="The testing center must be a central location with a clear traffic flow pattern to avoid "
                            "mixing at entrance and exit. Signs should make the flow pattern clear."
                            "<br>"
                            "Depending on the number to be tested and the time required, it is possible that a testing "
                            "center could be made available only one day a week, which would ensure availability of "
                            "that space for other activities the rest of the week. If that is the case, thorough "
                            "cleaning should be performed before and after the testing center is run."))

        self.tree.create_node(
            tag="How often will you test",
            identifier="5",
            parent="1a",
            data=Resource(
                explanation="Testing frequency can vary based on practicalities, including availability of tests. "
                            "Weekly testing would be the minimum for reliable detection of infectious individuals; "
                            "daily or biweekly would be preferred."
                            "<br>"
                            "It is possible to use varied testing frequency effectively. For instance, high-risk "
                            "individuals (such as those in team sports) may require more frequent testing. If test "
                            "supplies are limited, more frequent testing of teachers, especially those in contact "
                            "with a larger number of students, could be used."))

        self.tree.create_node(
            tag="How will you share the test results",
            identifier="6",
            parent="1a",
            data=Resource(
                explanation="When you test, the results of the tests will need to be reported. At the very least, "
                            "parents will need to be informed of their child’s results and staff will need to be "
                            "informed of their own results. You may need to check with your local Public Health "
                            "department to determine your responsibility for sharing results with them."))
        self.tree.create_node(
            tag="With parents/staff",
            identifier="6a",
            parent="6",
            data=Resource(
                explanation="You cannot provide medical test results directly to minors, so student results will need "
                            "to be shared with parents. However, because medical test results are protected "
                            "information, the means by which you share results must be HIPAA-compliant. You should "
                            "work with your test provider to determine the best method. "
                            "<br>"
                            "Here are some options:"
                            "<li>Email: Be aware that most email providers are NOT HIPAA-compliant. However, there are "
                            "paid end-to-end encryption services that can provide the appropriate protections</li>"
                            "<li>Online portal: often medical providers will send an email informing the patient or "
                            "their authorized representative that results are available on a password-protected</li>"
                            "<li>App: Several organizations have created phone-based apps for relaying test results "
                            "securely</li>"
                            "<li>Text message: Like email, most texting is NOT HIPAA-compliant, but there are paid "
                            "services that can provide appropriate protections</li>"
                            "<li>Phone call: A direct phone call to the number on record is appropriate if the "
                            "recipient has consented to receive results by phone. The call should begin with name and"
                            " contact details, and should be short. If the caller reaches voicemail, they must leave "
                            "a toll-free number that can be called to receive results.</li>"
                            "<br>"
                            "When deciding on a communications strategy, remember the need for accessibility. "
                            "Online or smartphone systems will not be available to those with limited internet "
                            "access. Often, multiple contact methods can be combined, with parents choosing their "
                            "preferred method."))

        self.tree.create_node(
            tag="With Public Health",
            identifier="6b",
            parent="6",
            data=Resource(
                explanation="If you are working with a medical laboratory, they will be reporting test results "
                            "directly to Public Health. It would be good to discuss this process with them, so you "
                            "are aware of their procedures."
                            "<br>"
                            "If you are using in-house rapid tests, you may be responsible for reporting to Public "
                            "Health. It is best to contact your local Public Health department as you are making your "
                            "plans so you know the information you must report, the method of reporting, and your "
                            "legal obligations."))

        self.tree.create_node(
            tag="With the community",
            identifier="6c",
            parent="6",
            data=Resource(
                explanation="Your school community, and the community at large, will want to know about cases within "
                            "your school. How you inform them can vary, but it must, at minimum, preserve the privacy "
                            "of any detected cases. That means that information should be shared publicly only in such "
                            "a way that the identity of a case cannot be deduced. In a small school, or with specialty"
                            " teachers and coaches, that can be extremely difficult."
                            "<br>"
                            "Aggregation is the best technique to use to preserve privacy. This refers to reporting "
                            "results only among groups; for instance, you might report only the grade of a student "
                            "testing positive."))

        self.tree.create_node(
            tag="With close contacts",
            identifier="6d",
            parent="6",
            data=Resource(
                explanation="When a positive case has been found, Public Health will often perform contact tracing, "
                            "in which any close contacts are informed 1) that they may have been exposed, 2) the day "
                            "of the exposure, and 3) the regulations regarding quarantine. You should contact your "
                            "local Public Health district to determine if you can help with their contact tracing "
                            "process."
                            "<br>"
                            "If your local Public Health department is not currently performing contact tracing, it "
                            "will fall to you to determine if anyone within your school should be notified of a "
                            "potential exposure. The CDC definition of a close contact is someone who has spent at "
                            "least 15 minutes (cumulative) within 6 feet of the infected individual between 48 hours "
                            "prior to their diagnosis or the start of their symptoms and the start of their "
                            "isolation. Among small children, that may be impossible to determine; quarantine of an "
                            "entire class would be a strong precaution but might be justified."
                            "<br>"
                            "One tension between preserving privacy and protecting health will arise with those who "
                            "are able to identify the potential case. Teachers will likely fall into this category – "
                            "they will recognize the student who is missing from their class. However, it is good "
                            "practice to inform teachers that a student of theirs has tested positive, as they may "
                            "need to take extra precautions to protect their family members."))

        self.tree.create_node(
            tag="Which test will you use",
            identifier="7",
            parent="1a",
            data=Resource(
                explanation="What test is available to you? A summary of tests and their uses is available here. The "
                            "test you select will determine the supplies you need, the speed at which results come, "
                            "and the cost."))

        self.tree.create_node(
            tag="What sample type will you need to collect",
            identifier="7a",
            parent="7",
            data=Resource(
                explanation="You will likely need either saliva or a nasal swab. Both can be self-collected, although "
                            "younger students may struggle with self-collection. A nasal swab can also be collected "
                            "by a health professional."
                            "<br>"
                            "If collecting nasal swabs, be aware that nose bleeds can occur. Have a protocol in place "
                            "(example here) for dealing with nose bleeds."
                            "<br>"
                            "If collecting saliva, some individuals struggle with sufficient saliva production. "
                            "Privacy may be needed by some. Others will need a testing exemption or an alternative, "
                            "as several medical conditions can interfere."))

        self.tree.create_node(
            tag="How fast will you get results",
            identifier="7b",
            parent="7",
            data=Resource(
                explanation="A test with a long delay may not be of use. If test reporting delays will be longer than "
                            "a few days, you may want to reconsider your testing program."))

        self.tree.create_node(
            tag="What will the cost be",
            identifier="7c",
            parent="7",
            data=Resource(
                explanation="Remember that the cost of testing includes supplies, personnel time, the laboratory "
                            "process, and the reporting mechanism. Ensure that you are sufficiently funded to cover "
                            "all aspects of the cost before deciding how many tests you are able to perform."))

        self.tree.create_node(
            tag="Will you use pooling",
            identifier="7d",
            parent="7",
            data=Resource(
                explanation="It is possible to test groups of samples (pools) together. If any pool tests positive, "
                            "the individuals within the pool (or their samples) should then be individually tested to "
                            "identify the infected person(s). This will result in slightly slower test turn-around, "
                            "but will greatly reduce costs."
                            "<br>"
                            "This will require a creation of pool groups that is sensible. Pools should be 3-5 "
                            "people in size, so multiple pools per class/pod may be required. You will need to work "
                            "with the lab to determine if pooling should be done at the sample collection or at the "
                            "lab."))


if __name__ == "__main__":
    testing_decision_tree = Testing_Decision_Tree()
    testing_decision_tree.tree.show()

    # get node given id
    current = testing_decision_tree.tree.get_node("2b")
    print("current:", vars(current.data))

    # check if it's the end
    print("is the end:", current.is_leaf())

    # list all the options
    options_pointers= current.fpointer
    print(testing_decision_tree.tree.children("2b"))

    # going back to last step
    print(testing_decision_tree.tree.children(current.bpointer))

    print(testing_decision_tree.tree.root)

    # test when submit find it's path
    print("\nstart traversing...")
    for node in testing_decision_tree.tree.rsearch(nid="3a"):
        print(node)
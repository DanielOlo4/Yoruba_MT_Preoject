# ================================================================
# DATASET STRUCTURE
# ================================================================

education_dataset = {

    # ============================================================
    # SECTION 1: SIMPLE SENTENCES - CLASSROOM GREETINGS & ROUTINES
    # ============================================================

    "greetings_and_routines": [
        # Basic Greetings
        {"english": "Good morning, teacher.", "yoruba": "E káàárọ̀, olùkọ́."},
        {"english": "Good afternoon, teacher.", "yoruba": "E kú àsán, olùkọ́."},
        {"english": "Good evening, teacher.", "yoruba": "E kú ìrọ̀lẹ́, olùkọ́."},
        {"english": "Good morning, students.", "yoruba": "E káàárọ̀, àwọn akẹ́kọ̀ọ́."},
        {"english": "Good afternoon, students.", "yoruba": "E kú àsán, àwọn akẹ́kọ̀ọ́."},
        {"english": "Good morning, class.", "yoruba": "E káàárọ̀, kíláàsì."},
        {"english": "Welcome to school.", "yoruba": "E kú àbọ̀ sí ilé ẹ̀kọ́."},
        {"english": "Welcome to class.", "yoruba": "E kú àbọ̀ sí kíláàsì."},
        {"english": "How are you?", "yoruba": "Báwo ni?"},
        {"english": "I am fine.", "yoruba": "Mo wà dáadáa."},
        {"english": "We are fine.", "yoruba": "A wà dáadáa."},
        {"english": "Thank you, teacher.", "yoruba": "E ṣé, olùkọ́."},
        {"english": "You are welcome.", "yoruba": "E kú àbọ̀."},
        {"english": "Goodbye, teacher.", "yoruba": "O dàbọ̀, olùkọ́."},
        {"english": "Goodbye, students.", "yoruba": "E o dàbọ̀, àwọn akẹ́kọ̀ọ́."},
        {"english": "See you tomorrow.", "yoruba": "A ó rí wa lọ́la."},
        {"english": "Have a nice day.", "yoruba": "E ní ọjọ́ tó dára."},
        {"english": "Good night.", "yoruba": "O dáàrọ̀."},
        {"english": "How is school today?", "yoruba": "Báwo ni ilé ẹ̀kọ́ lónìí?"},
        {"english": "School is fine today.", "yoruba": "Ilé ẹ̀kọ́ dára lónìí."},
        {"english": "Welcome back to school.", "yoruba": "E kú àtúnpadà sí ilé ẹ̀kọ́."},
        {"english": "Happy new term.", "yoruba": "E kú ọdún tuntun ẹ̀kọ́."},
        {"english": "Happy resumption.", "yoruba": "E kú àtúnpadà."},
        {"english": "How was your holiday?", "yoruba": "Báwo ni ìsinmi yín?"},
        {"english": "My holiday was fine.", "yoruba": "Ìsinmi mi dára."},
        {"english": "Adesewa is here.", "yoruba": "Adesewa wà níbí."},
        {"english": "I am here", "yoruba": "Mo wà níbí."},
        {"english": "He is here.", "yoruba": " Ó wà níbí."},

        # Daily Routines
        {"english": "Stand up.", "yoruba": "E dìde."},
        {"english": "Sit down.", "yoruba": "E jókòó."},
        {"english": "Come in.", "yoruba": "E wọlé."},
        {"english": "Go out.", "yoruba": "E jáde."},
        {"english": "Be quiet.", "yoruba": "E dákẹ́."},
        {"english": "Keep quiet.", "yoruba": "E pa ẹnu yín mọ́."},
        {"english": "Pay attention.", "yoruba": "E gbọ́ dáadáa."},
        {"english": "Listen carefully.", "yoruba": "E fi etí sílẹ̀ dáadáa."},
        {"english": "Look at the board.", "yoruba": "E wo pátákó."},
        {"english": "Look at me.", "yoruba": "E wò mí."},
        {"english": "Come here.", "yoruba": "Wá ibí."},
        {"english": "Go back to your seat.", "yoruba": "Padà sí ibùjókòó rẹ."},
        {"english": "Raise your hand.", "yoruba": "Gbé ọwọ́ rẹ sókè."},
        {"english": "Put your hand down.", "yoruba": "Sọ ọwọ́ rẹ kalẹ̀."},
        {"english": "Open your book.", "yoruba": "Ṣí ìwé rẹ."},
        {"english": "Close your book.", "yoruba": "Pa ìwé rẹ dé."},
        {"english": "Open your notebook.", "yoruba": "Ṣí ìwé àkọsílẹ̀ rẹ."},
        {"english": "Turn to page ten.", "yoruba": "Yí sí ojú ewé kẹwàá."},
        {"english": "Read the passage.", "yoruba": "Ka ẹ̀kọ́ náà."},
        {"english": "Write your name.", "yoruba": "Kọ orúkọ rẹ."},
        {"english": "Copy the notes.", "yoruba": "Ṣe àdàkọ àkọsílẹ̀ náà."},
        {"english": "Submit your work.", "yoruba": "Fi iṣẹ́ rẹ sílẹ̀."},
        {"english": "Collect your papers.", "yoruba": "Gba àwọn ìwé yín."},
        {"english": "Line up.", "yoruba": "E dúró ní ìtò."},
        {"english": "Form a line.", "yoruba": "Ṣe ìtò kan."},
        {"english": "March to class.", "yoruba": "Rin sí kíláàsì."},
        {"english": "Clean the board.", "yoruba": "Nù pátákó náà."},
        {"english": "Erase the board.", "yoruba": "Pa pátákó náà rẹ́."},
        {"english": "Pick up the chalk.", "yoruba": "Gbé kọ́ọ̀kì sókè."},
        {"english": "Pick up the duster.", "yoruba": "Gbé àfọ̀nù sókè."},
        {"english": "Bring your homework.", "yoruba": "Mú iṣẹ́ ilé rẹ wá."},
        {"english": "Do your assignment.", "yoruba": "Ṣe iṣẹ́ àṣẹ rẹ."},
        {"english": "Finish your work.", "yoruba": "Parí iṣẹ́ rẹ."},
        {"english": "Stop talking.", "yoruba": "Dẹ́kun ọ̀rọ̀ sísọ."},
        {"english": "Stop making noise.", "yoruba": "Dẹ́kun ariwo."},
        {"english": "Be orderly.", "yoruba": "E wà ní ìtò."},
        {"english": "Be disciplined.", "yoruba": "E ní ìwà rere."},
        {"english": "Behave yourself.", "yoruba": "Hùwà dáadáa."},
        {"english": "Clap your hands.", "yoruba": "E pa ọwọ́."},
        {"english": "Say the prayer.", "yoruba": "Kí àdúrà."},
        {"english": "Sing the anthem.", "yoruba": "Kọ orin ìyìn."},
    ],

    # ============================================================
    # SECTION 2: SIMPLE SENTENCES - CLASSROOM OBJECTS & MATERIALS
    # ============================================================

    "classroom_objects": [
        {"english": "This is a book.", "yoruba": "Èyí ni ìwé."},
        {"english": "That is a pen.", "yoruba": "Ìyẹn ni kálámù."},
        {"english": "This is a pencil.", "yoruba": "Èyí ni pẹ́ńsúlù."},
        {"english": "That is a ruler.", "yoruba": "Ìyẹn ni rúlà."},
        {"english": "This is an eraser.", "yoruba": "Èyí ni rọ́bà."},
        {"english": "That is a sharpener.", "yoruba": "Ìyẹn ni ohun mímu."},
        {"english": "This is a desk.", "yoruba": "Èyí ni tébùrù."},
        {"english": "That is a chair.", "yoruba": "Ìyẹn ni àga."},
        {"english": "This is the blackboard.", "yoruba": "Èyí ni pátákó dúdú."},
        {"english": "That is the whiteboard.", "yoruba": "Ìyẹn ni pátákó funfun."},
        {"english": "This is chalk.", "yoruba": "Èyí ni kọ́ọ̀kì."},
        {"english": "That is a marker.", "yoruba": "Ìyẹn ni máàkà."},
        {"english": "This is a notebook.", "yoruba": "Èyí ni ìwé àkọsílẹ̀."},
        {"english": "That is a textbook.", "yoruba": "Ìyẹn ni ìwé ẹ̀kọ́."},
        {"english": "This is a dictionary.", "yoruba": "Èyí ni ìwé atúmọ̀ èdè."},
        {"english": "That is a map.", "yoruba": "Ìyẹn ni àwòrán ilẹ̀."},
        {"english": "This is a globe.", "yoruba": "Èyí ni ayé ìṣàpẹẹrẹ."},
        {"english": "That is a computer.", "yoruba": "Ìyẹn ni kọ̀ǹpútà."},
        {"english": "This is a calculator.", "yoruba": "Èyí ni ẹ̀rọ ìṣírò."},
        {"english": "Where is my bag?", "yoruba": "Níbo ni àpò mi wà?"},
        {"english": "My bag is on the desk.", "yoruba": "Àpò mi wà lórí tébùrù."},
        {"english": "The pen is on the table.", "yoruba": "Kálámù wà lórí tébùrù."},
        {"english": "The books are in the bag.", "yoruba": "Àwọn ìwé wà nínú àpò."},
        {"english": "The chalk is on the board.", "yoruba": "Kọ́ọ̀kì wà lórí pátákó."},
        {"english": "I need a pen.", "yoruba": "Mo nílò kálámù."},
        {"english": "I need a notebook.", "yoruba": "Mo nílò ìwé àkọsílẹ̀."},
        {"english": "Give me the ruler.", "yoruba": "Fún mi ní rúlà."},
        {"english": "Pass me the eraser.", "yoruba": "Fà rọ́bà wá fún mi."},
        {"english": "I forgot my book at home.", "yoruba": "Mo gbàgbé ìwé mi sí ilé."},
        {"english": "I lost my pencil.", "yoruba": "Mo sọnù pẹ́ńsúlù mi."},
        {"english": "The classroom is clean.", "yoruba": "Kíláàsì mọ́."},
        {"english": "The classroom is dirty.", "yoruba": "Kíláàsì dọ̀tí."},
        {"english": "The board is clean.", "yoruba": "Pátákó mọ́."},
        {"english": "Bring the exercise book.", "yoruba": "Mú ìwé àdánwò wá."},
        {"english": "Use the blue pen.", "yoruba": "Lo kálámù aláwọ̀ búlúù."},
        {"english": "Use the red pen.", "yoruba": "Lo kálámù aláwọ̀ pupa."},
        {"english": "I have a new uniform.", "yoruba": "Mo ní àṣọ ilé ẹ̀kọ́ tuntun."},
        {"english": "The school uniform is white.", "yoruba": "Àṣọ ilé ẹ̀kọ́ jẹ́ funfun."},
        {"english": "Keep your materials ready.", "yoruba": "Fi ohun èlò rẹ sí ìpèsè."},
        {"english": "Arrange your desks.", "yoruba": "Tò àwọn tébùrù yín."},
    ],

    # ============================================================
    # SECTION 3: SIMPLE SENTENCES - SUBJECTS & ACADEMIC ACTIVITIES
    # ============================================================

    "subjects_and_academics": [
        {"english": "We are learning mathematics.", "yoruba": "A ń kọ́ ìṣírò."},
        {"english": "I like mathematics.", "yoruba": "Mo fẹ́ràn ìṣírò."},
        {"english": "Mathematics is interesting.", "yoruba": "Ìṣírò dùn mọ́ni."},
        {"english": "English is my best subject.", "yoruba": "Èdè Gẹ̀ẹ́sì ni ẹ̀kọ́ tí mo fẹ́ràn jù."},
        {"english": "We study Yoruba language.", "yoruba": "A ń kọ́ èdè Yorùbá."},
        {"english": "I love Yoruba language.", "yoruba": "Mo nífẹ̀ẹ́ èdè Yorùbá."},
        {"english": "Science is important.", "yoruba": "Sáyẹ́ǹsì ṣe pàtàkì."},
        {"english": "We have science class today.", "yoruba": "A ní ẹ̀kọ́ sáyẹ́ǹsì lónìí."},
        {"english": "History teaches us about the past.", "yoruba": "Ìtàn kọ́ wa nípa ohun tí ó ti ṣẹlẹ̀."},
        {"english": "Geography is about the earth.", "yoruba": "Jẹ́ọ́gírápì jẹ́ nípa ilẹ̀ ayé."},
        {"english": "We study social studies.", "yoruba": "A ń kọ́ ẹ̀kọ́ ìlú."},
        {"english": "We study civic education.", "yoruba": "A ń kọ́ ẹ̀kọ́ ọmọlúàbí."},
        {"english": "Art is creative.", "yoruba": "Iṣẹ́ ọnà jẹ́ aládàáṣe."},
        {"english": "Music is enjoyable.", "yoruba": "Orin dùn mọ́ni."},
        {"english": "Physical education keeps us healthy.", "yoruba": "Ẹ̀kọ́ eré ìdárayá jẹ́ kí a ní ìlera."},
        {"english": "We have physical education today.", "yoruba": "A ní ẹ̀kọ́ eré ìdárayá lónìí."},
        {"english": "Computer studies is modern.", "yoruba": "Ẹ̀kọ́ kọ̀ǹpútà jẹ́ ti ìgbàlódé."},
        {"english": "Agriculture teaches us about farming.", "yoruba": "Ẹ̀kọ́ iṣẹ́ àgbẹ̀ kọ́ wa nípa àgbẹ̀."},
        {"english": "I study biology.", "yoruba": "Mo ń kọ́ ẹ̀kọ́ nípa àwọn ohun alààyè."},
        {"english": "Chemistry is about chemical reactions.", "yoruba": "Kẹ́mísírì jẹ́ nípa ìyípadà kẹ́míkà."},
        {"english": "Physics is about forces and energy.", "yoruba": "Físíìkì jẹ́ nípa agbára àti okun."},
        {"english": "I study economics.", "yoruba": "Mo ń kọ́ ẹ̀kọ́ ètò ọrọ̀ ajé."},
        {"english": "Literature is about books and stories.", "yoruba": "Lítíréṣọ̀ jẹ́ nípa ìwé àti ìtàn."},
        {"english": "We read Yoruba literature.", "yoruba": "A ń ka lítíréṣọ̀ Yorùbá."},
        {"english": "Religious studies is important.", "yoruba": "Ẹ̀kọ́ ìsìn ṣe pàtàkì."},
        {"english": "We learn French.", "yoruba": "A ń kọ́ èdè Faransé."},
        {"english": "Arabic is another language.", "yoruba": "Lárúbáwá jẹ́ èdè mìíràn."},
        {"english": "I study home economics.", "yoruba": "Mo ń kọ́ ẹ̀kọ́ ìṣàkóso ilé."},
        {"english": "Technical drawing is a skill.", "yoruba": "Ìyàwòrán tẹ̀kníkà jẹ́ ọgbọ́n."},
        {"english": "The timetable is ready.", "yoruba": "Àtò àkókò ti ṣetán."},
        {"english": "What subject is next?", "yoruba": "Ẹ̀kọ́ wo ni ó kàn?"},
        {"english": "The next class is English.", "yoruba": "Kíláàsì tó kàn ni Gẹ̀ẹ́sì."},
        {"english": "We have six subjects today.", "yoruba": "A ní ẹ̀kọ́ mẹ́fà lónìí."},
        {"english": "I scored high marks in mathematics.", "yoruba": "Mo gba àmì gíga ní ìṣírò."},
        {"english": "She passed all her subjects.", "yoruba": "Ó kọjá gbogbo ẹ̀kọ́ rẹ̀."},
        {"english": "He failed the examination.", "yoruba": "Ó kùnà ní ìdánwò."},
        {"english": "The results are out.", "yoruba": "Èsì ti jáde."},
        {"english": "I came first in class.", "yoruba": "Mo wá ní ipò kìíní nínú kíláàsì."},
        {"english": "She is the best student.", "yoruba": "Òun ni akẹ́kọ̀ọ́ tó dára jù."},
        {"english": "The lesson is over.", "yoruba": "Ẹ̀kọ́ ti parí."},
        {"english": "I understand.", "yoruba": "Ó yé mi."},
    ],

    # ============================================================
    # SECTION 4: SIMPLE SENTENCES - TEACHER INSTRUCTIONS
    # ============================================================

    "teacher_instructions": [
        {"english": "Repeat after me.", "yoruba": "E tún sọ lẹ́yìn mi."},
        {"english": "Say it again.", "yoruba": "Sọ ọ́ lẹ́ẹ̀kansi."},
        {"english": "Speak louder.", "yoruba": "Sọ̀rọ̀ ní ohùn tó ga."},
        {"english": "Speak clearly.", "yoruba": "Sọ̀rọ̀ kedere."},
        {"english": "Read aloud.", "yoruba": "Ka ní ohùn rara."},
        {"english": "Read silently.", "yoruba": "Ka ní ìdákẹ́rọ́rọ́."},
        {"english": "Write in your notebook.", "yoruba": "Kọ sínú ìwé àkọsílẹ̀ rẹ."},
        {"english": "Write neatly.", "yoruba": "Kọ lẹ́tà tó mọ́yàn."},
        {"english": "Draw a line.", "yoruba": "Fa ìlà kan."},
        {"english": "Draw a circle.", "yoruba": "Ya oṣùpá kan."},
        {"english": "Color the picture.", "yoruba": "Fi àwọ̀ kún àwòrán náà."},
        {"english": "Answer the question.", "yoruba": "Dáhùn ìbéèrè náà."},
        {"english": "Ask a question.", "yoruba": "Bi ìbéèrè kan."},
        {"english": "Think carefully.", "yoruba": "Rò ó dáadáa."},
        {"english": "Try again.", "yoruba": "Gbìyànjú lẹ́ẹ̀kansi."},
        {"english": "Do not give up.", "yoruba": "Má ṣe jáwọ́."},
        {"english": "Work in groups.", "yoruba": "Ṣiṣẹ́ ní ẹgbẹ́."},
        {"english": "Work in pairs.", "yoruba": "Ṣiṣẹ́ ní méjì méjì."},
        {"english": "Work alone.", "yoruba": "Ṣiṣẹ́ fúnra rẹ."},
        {"english": "Share with your partner.", "yoruba": "Pín pẹ̀lú alábàáṣiṣẹ́ rẹ."},
        {"english": "Help your friend.", "yoruba": "Ràn ọ̀rẹ́ rẹ lọ́wọ́."},
        {"english": "Do not cheat.", "yoruba": "Má ṣe jìbìtì."},
        {"english": "Do not copy.", "yoruba": "Má ṣe dá iṣẹ́ ẹlòmíràn kọ."},
        {"english": "Study hard.", "yoruba": "Kàwé gidigidi."},
        {"english": "Practice every day.", "yoruba": "Ṣe àdánrawò lójoojúmọ́."},
        {"english": "Do your best.", "yoruba": "Ṣe ohun tó dára jù tí o lè ṣe."},
        {"english": "Explain your answer.", "yoruba": "Ṣàlàyé ìdáhùn rẹ."},
        {"english": "Correct your mistakes.", "yoruba": "Ṣàtúnṣe àṣìṣe rẹ."},
        {"english": "Check your work.", "yoruba": "Yẹ iṣẹ́ rẹ wò."},
        {"english": "Compare your answers.", "yoruba": "Fi àwọn ìdáhùn rẹ wé ara wọn."},
        {"english": "Memorize this poem.", "yoruba": "Kọ́ ewì yìí."},
        {"english": "Recite the poem.", "yoruba": "Ka ewì náà."},
        {"english": "Spell the word.", "yoruba": "Pe ọ̀rọ̀ náà lẹ́tà lẹ́tà."},
        {"english": "Define the word.", "yoruba": "Ṣàlàyé ìtumọ̀ ọ̀rọ̀ náà."},
        {"english": "Use the word in a sentence.", "yoruba": "Lo ọ̀rọ̀ náà nínú gbólóhùn."},
        {"english": "Translate this sentence.", "yoruba": "Túmọ̀ gbólóhùn yìí."},
        {"english": "Summarize the passage.", "yoruba": "Ṣàkópọ̀ ẹ̀kọ́ náà."},
        {"english": "Write a composition.", "yoruba": "Kọ àròkọ kan."},
        {"english": "Write an essay.", "yoruba": "Kọ ẹsè kan."},
        {"english": "Read the instructions.", "yoruba": "Ka àwọn ìtọ́sọ́nà."},
        {"english": "Follow the instructions.", "yoruba": "Tẹ̀lé àwọn ìtọ́sọ́nà."},
        {"english": "Underline the correct answer.", "yoruba": "Fa ìlà sí àbẹ́ ìdáhùn tó tọ́."},
        {"english": "Circle the right answer.", "yoruba": "Ya oṣùpá yí ìdáhùn tó tọ́ ká."},
        {"english": "Fill in the blanks.", "yoruba": "Kún àwọn àyè tó ṣófo."},
        {"english": "Match the words.", "yoruba": "So àwọn ọ̀rọ̀ pọ̀."},
        {"english": "Complete the exercise.", "yoruba": "Parí àdánwò náà."},
        {"english": "Solve the problem.", "yoruba": "Yanjú ìṣòro náà."},
        {"english": "Calculate the answer.", "yoruba": "Ṣe ìṣírò ìdáhùn náà."},
        {"english": "Count the numbers.", "yoruba": "Kà àwọn nọ́ńbà náà."},
        {"english": "Measure the length.", "yoruba": "Wọn gígùn náà."},
        {"english": "Add these numbers.", "yoruba": "Fi àwọn nọ́ńbà yìí papọ̀."},
        {"english": "Subtract five from ten.", "yoruba": "Yọ àrún kúrò nínú ẹ̀wàá."},
        {"english": "Multiply three by four.", "yoruba": "Ìsọdipúpọ̀ mẹ́ta ní ẹ̀ẹ̀mẹ́rin."},
        {"english": "Divide twenty by five.", "yoruba": "Pín ogún sí àrún."},
        {"english": "Show your working.", "yoruba": "Fi ọ̀nà iṣẹ́ rẹ hàn."},
    ],

    # ============================================================
    # SECTION 5: SIMPLE SENTENCES - STUDENT EXPRESSIONS
    # ============================================================

    "student_expressions": [
        {"english": "I understand.", "yoruba": "Mo yé mi."},
        {"english": "I do not understand.", "yoruba": "Kò yé mi."},
        {"english": "Can you repeat that?", "yoruba": "Ṣé e lè tún sọ ọ́?"},
        {"english": "Please explain again.", "yoruba": "Ẹ jọ̀wọ́, ṣàlàyé lẹ́ẹ̀kansi."},
        {"english": "I have a question.", "yoruba": "Mo ní ìbéèrè kan."},
        {"english": "May I ask a question?", "yoruba": "Ṣé mo lè bi ìbéèrè?"},
        {"english": "I know the answer.", "yoruba": "Mo mọ ìdáhùn náà."},
        {"english": "I do not know the answer.", "yoruba": "Mi ò mọ ìdáhùn náà."},
        {"english": "May I go to the toilet?", "yoruba": "Ṣé mo lè lọ sí ilé ìgbọ̀nsẹ̀?"},
        {"english": "May I drink water?", "yoruba": "Ṣé mo lè mu omi?"},
        {"english": "I am sorry I am late.", "yoruba": "E má bínú, mo pẹ́."},
        {"english": "I am ready.", "yoruba": "Mo ti ṣetán."},
        {"english": "I am not ready.", "yoruba": "Mi ò tíì ṣetán."},
        {"english": "I have finished.", "yoruba": "Mo ti parí."},
        {"english": "I have not finished.", "yoruba": "Mi ò tíì parí."},
        {"english": "I need help.", "yoruba": "Mo nílò ìrànlọ́wọ́."},
        {"english": "Please help me.", "yoruba": "Ẹ jọ̀wọ́, ẹ ràn mí lọ́wọ́."},
        {"english": "I forgot.", "yoruba": "Mo gbàgbé."},
        {"english": "I remember now.", "yoruba": "Mo rántí báyìí."},
        {"english": "This is difficult.", "yoruba": "Èyí ṣòro."},
        {"english": "This is easy.", "yoruba": "Èyí rọrùn."},
        {"english": "I am confused.", "yoruba": "Inú mi dàrú."},
        {"english": "I made a mistake.", "yoruba": "Mo ṣe àṣìṣe."},
        {"english": "I am sorry.", "yoruba": "E máa bínú."},
        {"english": "Thank you for teaching us.", "yoruba": "E ṣé fún ẹ̀kọ́ tí ẹ kọ́ wa."},
        {"english": "May I borrow your pen?", "yoruba": "Ṣé mo lè yá kálámù rẹ?"},
        {"english": "May I go out?", "yoruba": "Ṣé mo lè jáde?"},
        {"english": "I am sick.", "yoruba": "Ara mi kò yá."},
        {"english": "I have a headache.", "yoruba": "Orí ń fò mí."},
        {"english": "I am hungry.", "yoruba": "Ebi ń pa mí."},
        {"english": "I am thirsty.", "yoruba": "Òùngbẹ ń gbẹ mí."},
        {"english": "I agree.", "yoruba": "Mo gbà."},
        {"english": "I disagree.", "yoruba": "Mi ò gbà."},
        {"english": "I tried my best.", "yoruba": "Mo gbìyànjú gidigidi."},
        {"english": "I want to learn more.", "yoruba": "Mo fẹ́ kọ́ ẹ̀kọ́ síi."},
        {"english": "Can I start again?", "yoruba": "Ṣé mo lè tún bẹ̀rẹ̀?"},
        {"english": "I will study harder.", "yoruba": "Èmi yóò kàwé gidigidi."},
        {"english": "I promise to be better.", "yoruba": "Mo ṣèlérí pé èmi yóò dára sí i."},
        {"english": "I am present.", "yoruba": "Mo wà níbí."},
        {"english": "I was absent yesterday.", "yoruba": "Mi ò wá lánàá."},
    ],

    # ============================================================
    # SECTION 6: SIMPLE SENTENCES - SCHOOL ENVIRONMENT
    # ============================================================

    "school_environment": [
        {"english": "The school is big.", "yoruba": "Ilé ẹ̀kọ́ tóbi."},
        {"english": "The school is small.", "yoruba": "Ilé ẹ̀kọ́ kéré."},
        {"english": "The school is beautiful.", "yoruba": "Ilé ẹ̀kọ́ lẹ́wà."},
        {"english": "The library has many books.", "yoruba": "Ilé ìkàwé ní ìwé púpọ̀."},
        {"english": "I go to the library.", "yoruba": "Mo lọ sí ilé ìkàwé."},
        {"english": "The laboratory is well equipped.", "yoruba": "Ilé yàrá ìdánwò ní ohun èlò tó pé."},
        {"english": "The playground is large.", "yoruba": "Pápá eré tóbi."},
        {"english": "The children are playing.", "yoruba": "Àwọn ọmọdé ń ṣeré."},
        {"english": "The assembly ground is clean.", "yoruba": "Pápá àpéjọ mọ́."},
        {"english": "The principal is in the office.", "yoruba": "Olùdarí wà ní ọ́fíìsì."},
        {"english": "The teacher is in the staffroom.", "yoruba": "Olùkọ́ wà ní yàrá olùkọ́."},
        {"english": "The school has a gate.", "yoruba": "Ilé ẹ̀kọ́ ní ẹnubodè."},
        {"english": "The school has a fence.", "yoruba": "Ilé ẹ̀kọ́ ní odi."},
        {"english": "The school has a garden.", "yoruba": "Ilé ẹ̀kọ́ ní ọgbà."},
        {"english": "The canteen sells food.", "yoruba": "Ilé oúnjẹ ń ta oúnjẹ."},
        {"english": "Students eat during break.", "yoruba": "Àwọn akẹ́kọ̀ọ́ jẹun nígbà ìsinmi."},
        {"english": "Break time is thirty minutes.", "yoruba": "Àkókò ìsinmi jẹ́ ìṣẹ́jú ọgbọ̀n."},
        {"english": "School starts at eight o'clock.", "yoruba": "Ilé ẹ̀kọ́ bẹ̀rẹ̀ ní aago mẹ́jọ."},
        {"english": "School closes at two o'clock.", "yoruba": "Ilé ẹ̀kọ́ pa dé ní aago méjì."},
        {"english": "The bell is ringing.", "yoruba": "Agogo ń dún."},
        {"english": "The school flag is green and white.", "yoruba": "Àsíá ilé ẹ̀kọ́ jẹ́ ewé àti funfun."},
        {"english": "Our school has five hundred students.", "yoruba": "Ilé ẹ̀kọ́ wa ní ẹgbẹ̀rún márùn-ún akẹ́kọ̀ọ́."},
        {"english": "There are thirty students in our class.", "yoruba": "Akẹ́kọ̀ọ́ ọgbọ̀n ni wà nínú kíláàsì wa."},
        {"english": "The toilet is clean.", "yoruba": "Ilé ìgbọ̀nsẹ̀ mọ́."},
        {"english": "The school has electricity.", "yoruba": "Ilé ẹ̀kọ́ ní iná mọ̀nàmọ́ná."},
        {"english": "The school has water.", "yoruba": "Ilé ẹ̀kọ́ ní omi."},
        {"english": "The classroom has a fan.", "yoruba": "Kíláàsì ní fáánì."},
        {"english": "There are flowers in the school.", "yoruba": "Àwọn ìtànná wà ní ilé ẹ̀kọ́."},
        {"english": "The school is near my house.", "yoruba": "Ilé ẹ̀kọ́ súnmọ́ ilé mi."},
        {"english": "The school is far from my house.", "yoruba": "Ilé ẹ̀kọ́ jìnnà sí ilé mi."},
    ],

    # ============================================================
    # SECTION 7: SIMPLE SENTENCES - NUMBERS AND COUNTING
    # ============================================================

    "numbers_and_counting": [
        {"english": "One.", "yoruba": "Ọ̀kan."},
        {"english": "Two.", "yoruba": "Èjì."},
        {"english": "Three.", "yoruba": "Ẹ̀ta."},
        {"english": "Four.", "yoruba": "Ẹ̀rin."},
        {"english": "Five.", "yoruba": "Àrún."},
        {"english": "Six.", "yoruba": "Ẹ̀fà."},
        {"english": "Seven.", "yoruba": "Èje."},
        {"english": "Eight.", "yoruba": "Ẹ̀jọ."},
        {"english": "Nine.", "yoruba": "Ẹ̀sán."},
        {"english": "Ten.", "yoruba": "Ẹ̀wàá."},
        {"english": "Count from one to ten.", "yoruba": "Kà láti ọ̀kan sí ẹ̀wàá."},
        {"english": "Count from one to twenty.", "yoruba": "Kà láti ọ̀kan sí ogún."},
        {"english": "How many students are present?", "yoruba": "Àwọn akẹ́kọ̀ọ́ mélòó ni wọ́n wà?"},
        {"english": "Twenty students are present.", "yoruba": "Àwọn akẹ́kọ̀ọ́ ogún ni wọ́n wà."},
        {"english": "Five students are absent.", "yoruba": "Àwọn akẹ́kọ̀ọ́ márùn-ún kò wá."},
        {"english": "What is two plus three?", "yoruba": "Kín ni èjì pẹ̀lú ẹ̀ta?"},
        {"english": "Two plus three equals five.", "yoruba": "Èjì pẹ̀lú ẹ̀ta jẹ́ àrún."},
        {"english": "What is ten minus four?", "yoruba": "Kín ni ẹ̀wàá yọ ẹ̀rin?"},
        {"english": "Ten minus four equals six.", "yoruba": "Ẹ̀wàá yọ ẹ̀rin jẹ́ ẹ̀fà."},
        {"english": "What is three times five?", "yoruba": "Kín ni ẹ̀ta lẹ́ẹ̀ àrún?"},
        {"english": "Three times five equals fifteen.", "yoruba": "Ẹ̀ta lẹ́ẹ̀ àrún jẹ́ ẹ̀ẹ́dógún."},
        {"english": "Eleven.", "yoruba": "Ọ̀kànlá."},
        {"english": "Twelve.", "yoruba": "Èjìlá."},
        {"english": "Thirteen.", "yoruba": "Ẹ̀tàlá."},
        {"english": "Fourteen.", "yoruba": "Ẹ̀rìnlá."},
        {"english": "Fifteen.", "yoruba": "Ẹ̀ẹ́dógún."},
        {"english": "Twenty.", "yoruba": "Ogún."},
        {"english": "Thirty.", "yoruba": "Ọgbọ̀n."},
        {"english": "Forty.", "yoruba": "Ogójì."},
        {"english": "Fifty.", "yoruba": "Àádọ́ta."},
        {"english": "One hundred.", "yoruba": "Ọgọ́rùn-ún."},
        {"english": "One thousand.", "yoruba": "Ẹgbẹ̀rún."},
        {"english": "First.", "yoruba": "Àkọ́kọ́."},
        {"english": "Second.", "yoruba": "Èkejì."},
        {"english": "Third.", "yoruba": "Ẹ̀kẹta."},
        {"english": "Last.", "yoruba": "Ìkẹyìn."},
    ],

    # ============================================================
    # SECTION 8: SIMPLE SENTENCES - DAYS, TIME & CALENDAR
    # ============================================================

    "days_time_calendar": [
        {"english": "Today is Monday.", "yoruba": "Ọjọ́ yìí jẹ́ Ọjọ́ Àìkú."},
        {"english": "Tomorrow is Tuesday.", "yoruba": "Ọ̀la jẹ́ Ọjọ́ Ajé."},
        {"english": "Yesterday was Sunday.", "yoruba": "Àná jẹ́ Ọjọ́ Àìkú."},
        {"english": "Today is Wednesday.", "yoruba": "Ọjọ́ yìí jẹ́ Ọjọ́ Rú."},
        {"english": "Today is Thursday.", "yoruba": "Ọjọ́ yìí jẹ́ Ọjọ́bọ̀."},
        {"english": "Today is Friday.", "yoruba": "Ọjọ́ yìí jẹ́ Ọjọ́ Ẹtì."},
        {"english": "Tomorrow is Saturday.", "yoruba": "Ọ̀la jẹ́ Ọjọ́ Àbámẹ́ta."},
        {"english": "There is no school on Saturday.", "yoruba": "Kò sí ilé ẹ̀kọ́ ní Ọjọ́ Àbámẹ́ta."},
        {"english": "There is no school on Sunday.", "yoruba": "Kò sí ilé ẹ̀kọ́ ní Ọjọ́ Àìkú."},
        {"english": "What time is it?", "yoruba": "Aago mélòó ni?"},
        {"english": "It is eight o'clock.", "yoruba": "Aago mẹ́jọ ni."},
        {"english": "It is nine o'clock.", "yoruba": "Aago mẹ́sàn-án ni."},
        {"english": "It is time for class.", "yoruba": "Ó ti tó àkókò ẹ̀kọ́."},
        {"english": "It is break time.", "yoruba": "Àkókò ìsinmi ni."},
        {"english": "It is closing time.", "yoruba": "Àkókò ìpadé ni."},
        {"english": "The term begins in January.", "yoruba": "Ìgbà ẹ̀kọ́ bẹ̀rẹ̀ ní oṣù Kínní."},
        {"english": "The term ends in April.", "yoruba": "Ìgbà ẹ̀kọ́ parí ní oṣù Kẹrin."},
        {"english": "The examination is in June.", "yoruba": "Ìdánwò wà ní oṣù Okudu."},
        {"english": "The holiday starts in July.", "yoruba": "Ìsinmi bẹ̀rẹ̀ ní oṣù Agẹmọ."},
        {"english": "January is the first month.", "yoruba": "Oṣù Kínní ni oṣù àkọ́kọ́."},
        {"english": "December is the last month.", "yoruba": "Oṣù Bẹ́lú ni oṣù ìkẹyìn."},
        {"english": "There are twelve months in a year.", "yoruba": "Oṣù méjìlá wà nínú ọdún kan."},
        {"english": "There are seven days in a week.", "yoruba": "Ọjọ́ méje wà nínú ọ̀sẹ̀ kan."},
        {"english": "School reopens on Monday.", "yoruba": "Ilé ẹ̀kọ́ tún ṣí ní Ọjọ́ Àìkú."},
        {"english": "The new term starts next week.", "yoruba": "Ìgbà ẹ̀kọ́ tuntun bẹ̀rẹ̀ ní ọ̀sẹ̀ tó ń bọ̀."},
    ],

    # ============================================================
    # SECTION 9: COMPOUND SENTENCES - CLASSROOM ACTIVITIES
    # ============================================================

    "compound_sentences_classroom": [
        {"english": "Open your books and read the passage.",
         "yoruba": "Ṣí ìwé yín kí ẹ sì ka ẹ̀kọ́ náà."},
        {"english": "Stand up and greet the teacher.",
         "yoruba": "E dìde kí ẹ sì kí olùkọ́."},
        {"english": "The teacher came in and the students stood up.",
         "yoruba": "Olùkọ́ wọlé, àwọn akẹ́kọ̀ọ́ sì dìde."},
        {"english": "Read the question and write the answer.",
         "yoruba": "Ka ìbéèrè náà kí o sì kọ ìdáhùn."},
        {"english": "I studied hard and I passed the examination.",
         "yoruba": "Mo kàwé gidigidi, mo sì borí ìdánwò."},
        {"english": "She read the book and she understood the lesson.",
         "yoruba": "Ó ka ìwé náà, ó sì yé e lọ́kàn."},
        {"english": "The bell rang and the students went to class.",
         "yoruba": "Agogo dún, àwọn akẹ́kọ̀ọ́ sì lọ sí kíláàsì."},
        {"english": "The teacher explained the topic and asked questions.",
         "yoruba": "Olùkọ́ ṣàlàyé àkòrí náà, ó sì bi àwọn ìbéèrè."},
        {"english": "Write your name and submit your paper.",
         "yoruba": "Kọ orúkọ rẹ kí o sì fi ìwé rẹ sílẹ̀."},
        {"english": "I like science but I prefer mathematics.",
         "yoruba": "Mo fẹ́ràn sáyẹ́ǹsì ṣùgbọ́n mo fẹ́ràn ìṣírò ju."},
        {"english": "He is clever but he is lazy.",
         "yoruba": "Ó gbọ́n ṣùgbọ́n ó jẹ́ ọlẹ́."},
        {"english": "She passed English but she failed mathematics.",
         "yoruba": "Ó kọjá ní Gẹ̀ẹ́sì ṣùgbọ́n ó kùnà ní ìṣírò."},
        {"english": "The teacher is strict but she is fair.",
         "yoruba": "Olùkọ́ le ṣùgbọ́n ó ṣe déédéé."},
        {"english": "Study your notes or you will fail.",
         "yoruba": "Kà àkọsílẹ̀ rẹ tàbí ìwọ yóò kùnà."},
        {"english": "Come early or you will miss the lesson.",
         "yoruba": "Wá ní kùtùkùtù tàbí ìwọ yóò pàdánù ẹ̀kọ́."},
        {"english": "Bring your textbook or borrow one from a friend.",
         "yoruba": "Mú ìwé ẹ̀kọ́ rẹ wá tàbí yá ọ̀kan lọ́wọ́ ọ̀rẹ́."},
        {"english": "The students listened and they took notes.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ gbọ́ dáadáa, wọ́n sì kọ àkọsílẹ̀."},
        {"english": "Clean the board and arrange the chairs.",
         "yoruba": "Nù pátákó kí o sì tò àwọn àga."},
        {"english": "The examination was difficult but many students passed.",
         "yoruba": "Ìdánwò náà ṣòro ṣùgbọ́n ọ̀pọ̀lọpọ̀ akẹ́kọ̀ọ́ kọjá."},
        {"english": "He forgot his homework and the teacher punished him.",
         "yoruba": "Ó gbàgbé iṣẹ́ ilé rẹ̀, olùkọ́ sì jẹ ẹ́ níyà."},
        {"english": "The class was noisy so the teacher scolded them.",
         "yoruba": "Kíláàsì ṣe ariwo nítorí náà olùkọ́ bá wọn wí."},
        {"english": "I woke up early and I got to school on time.",
         "yoruba": "Mo jí ní kùtùkùtù, mo sì dé ilé ẹ̀kọ́ ní àkókò."},
        {"english": "She scored the highest marks and she received a prize.",
         "yoruba": "Ó gba àmì tó ga jù, ó sì gba ẹ̀bùn."},
        {"english": "The students sang and they danced during the cultural day.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ kọrin, wọ́n sì jó ní ọjọ́ àṣà."},
        {"english": "We read in the morning and we played in the afternoon.",
         "yoruba": "A ka ìwé ní àárọ̀ a sì ṣeré ní ọ̀sán."},
        {"english": "The teacher marked the scripts and recorded the scores.",
         "yoruba": "Olùkọ́ ṣàmì sí àwọn ìwé, ó sì kọ àwọn àmì sílẹ̀."},
        {"english": "The students were quiet and the lesson continued smoothly.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ dákẹ́, ẹ̀kọ́ sì tẹ̀síwájú dáadáa."},
        {"english": "I revised my notes and I practiced past questions.",
         "yoruba": "Mo tún àkọsílẹ̀ mi wò, mo sì ṣe àwọn ìbéèrè àtijọ́."},
        {"english": "He arrived late but the teacher allowed him in.",
         "yoruba": "Ó dé pẹ́ ṣùgbọ́n olùkọ́ jẹ́ kí ó wọlé."},
        {"english": "We completed the syllabus and we started revision.",
         "yoruba": "A parí ètò ẹ̀kọ́ a sì bẹ̀rẹ̀ àtúnyẹ̀wò."},
        {"english": "The school closed early and the students went home.",
         "yoruba": "Ilé ẹ̀kọ́ pa dé ní kùtùkùtù àwọn akẹ́kọ̀ọ́ sì lọ sílé."},
        {"english": "She borrowed a pen and she returned it after class.",
         "yoruba": "Ó yá kálámù, ó sì dá a padà lẹ́yìn ẹ̀kọ́."},
        {"english": "The teacher smiled and praised the student.",
         "yoruba": "Olùkọ́ rẹ́rìn-ín músẹ́ ó sì yìn akẹ́kọ̀ọ́ náà."},
        {"english": "I made a mistake but I corrected it.",
         "yoruba": "Mo ṣe àṣìṣe ṣùgbọ́n mo ṣàtúnṣe rẹ̀."},
        {"english": "We planted trees and watered them every day.",
         "yoruba": "A gbìn àwọn igi a sì mbomi wọn lójoojúmọ́."},
        {"english": "The principal spoke and the students listened attentively.",
         "yoruba": "Olùdarí sọ̀rọ̀ àwọn akẹ́kọ̀ọ́ sì fi etí sílẹ̀ dáadáa."},
    ],

    # ============================================================
    # SECTION 10: COMPOUND SENTENCES - ACADEMIC DISCUSSIONS
    # ============================================================

    "compound_sentences_academic": [
        {"english": "Mathematics is challenging but it is rewarding.",
         "yoruba": "Ìṣírò le ṣùgbọ́n ó san án."},
        {"english": "We learn grammar in English and we learn culture in Yoruba.",
         "yoruba": "A ń kọ́ gírámà ní Gẹ̀ẹ́sì, a sì ń kọ́ àṣà ní Yorùbá."},
        {"english": "The school has a library and it also has a laboratory.",
         "yoruba": "Ilé ẹ̀kọ́ ní ilé ìkàwé, ó sì tún ní ilé yàrá ìdánwò."},
        {"english": "The students read the text and discussed its main ideas.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ ka ẹsẹ̀ náà, wọ́n sì jíròrò àwọn èrò pàtàkì inú rẹ̀."},
        {"english": "If you study regularly, you will understand the lesson.",
         "yoruba": "Bí o bá ń kàwé déédéé, wàá lóye ẹ̀kọ́ náà."},
        {"english": "The teacher will assess the work before giving feedback.",
         "yoruba": "Olùkọ́ yóò yẹ iṣẹ́ náà wò kí ó tó fún wọn ní ìdáhùn."},
        {"english": "The students worked in groups, and each group presented its answer.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ ṣiṣẹ́ ní ẹgbẹ́ ẹgbẹ́, ẹgbẹ́ kọ̀ọ̀kan sì gbé ìdáhùn rẹ̀ kalẹ̀."},
        {"english": "The principal encouraged the students to work hard.",
         "yoruba": "Olùdarí gba àwọn akẹ́kọ̀ọ́ níyànjú láti ṣiṣẹ́ takuntakun."},
        {"english": "The library was quiet while the students were reading.",
         "yoruba": "Ilé ìkàwé dákẹ́ nígbà tí àwọn akẹ́kọ̀ọ́ ń kàwé."},
        {"english": "The teacher used examples so that the students could understand.",
         "yoruba": "Olùkọ́ lo àpẹẹrẹ kí àwọn akẹ́kọ̀ọ́ lè lóye."},
        {"english": "The students compared their answers before submitting their work.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ fiwera àwọn ìdáhùn wọn kí wọ́n tó fi iṣẹ́ wọn sílẹ̀."},
        {"english": "The school organised a debate, and the students spoke confidently.",
         "yoruba": "Ilé ẹ̀kọ́ ṣètò ìjíròrò, àwọn akẹ́kọ̀ọ́ sì sọ̀rọ̀ pẹ̀lú ìgbọ́kànlé."},
        {"english": "The teacher praised the student who answered correctly.",
         "yoruba": "Olùkọ́ yìn akẹ́kọ̀ọ́ tí ó dáhùn lọ́nà tó tọ́."},
        {"english": "We must respect one another because respect promotes learning.",
         "yoruba": "A gbọ́dọ̀ bọ̀wọ̀ fún ara wa nítorí ìbọ̀wọ̀ ń gbé ẹ̀kọ́ ga."},
        {"english": "The school provides a safe environment for teaching and learning.",
         "yoruba": "Ilé ẹ̀kọ́ ń pèsè àyíká ààbò fún kíkọ́ àti ẹ̀kọ́."},
    ],

    # ============================================================
    # SECTION 11: COMPLEX SENTENCES - LEARNING, VALUES & SCHOOL LIFE
    # ============================================================

    "complex_sentences_school_life": [
        {"english": "When the teacher enters the classroom, the students stand up.",
         "yoruba": "Nígbà tí olùkọ́ bá wọ kíláàsì, àwọn akẹ́kọ̀ọ́ máa ń dìde."},
        {"english": "Before you submit your work, check your answers carefully.",
         "yoruba": "Kí o tó fi iṣẹ́ rẹ sílẹ̀, yẹ àwọn ìdáhùn rẹ wò dáadáa."},
        {"english": "After the lesson ended, the students went home.",
         "yoruba": "Lẹ́yìn tí ẹ̀kọ́ parí, àwọn akẹ́kọ̀ọ́ lọ sílé."},
        {"english": "Because she studied hard, she passed the examination.",
         "yoruba": "Nítorí pé ó kàwé takuntakun, ó kọjá ìdánwò."},
        {"english": "If you do not understand, ask the teacher for help.",
         "yoruba": "Bí o kò bá lóye, béèrè fún ìrànlọ́wọ́ lọ́wọ́ olùkọ́."},
        {"english": "If we work together, we will complete the project on time.",
         "yoruba": "Bí a bá ṣiṣẹ́ pọ̀, a ó parí iṣẹ́ àgbékalẹ̀ náà ní àkókò."},
        {"english": "The student who came late explained why he was absent.",
         "yoruba": "Akẹ́kọ̀ọ́ tí ó dé pẹ́ ṣàlàyé ìdí tí kò fi wà níbẹ̀."},
        {"english": "The book that the teacher recommended is in the library.",
         "yoruba": "Ìwé tí olùkọ́ dámọ̀ràn wà nínú ilé ìkàwé."},
        {"english": "The class will begin when everybody is ready.",
         "yoruba": "Kíláàsì yóò bẹ̀rẹ̀ nígbà tí gbogbo ènìyàn bá ti múra tán."},
        {"english": "Even though he was tired, he completed his homework.",
         "yoruba": "Bí ó tilẹ̀ jẹ́ pé ó rẹ̀, ó parí iṣẹ́ ilé rẹ̀."},
        {"english": "The students remained in class until the teacher returned.",
         "yoruba": "Àwọn akẹ́kọ̀ọ́ dúró nínú kíláàsì títí olùkọ́ fi padà."},
         {"english": "Bolaji is a boy.",
                  "yoruba": "ọkùrin ni Bọ́lájí."},
        {"english": "We should keep the classroom clean so that everyone can learn comfortably.",
         "yoruba": "A yẹ kí a máa jẹ́ kí kíláàsì mọ́ kí gbogbo ènìyàn lè kọ́ ẹ̀kọ́ ní ìfẹ̀ẹ́."},
        {"english": "The student who reads every day improves quickly.",
         "yoruba": "Akẹ́kọ̀ọ́ tí ó ń kàwé lójoojúmọ́ máa ń tẹ̀síwájú kánkán."},
        {"english": "Although technology is useful, students must use it responsibly.",
         "yoruba": "Bí ó tilẹ̀ jẹ́ pé ìmọ̀ ẹ̀rọ wúlò, àwọn akẹ́kọ̀ọ́ gbọ́dọ̀ lò ó lọ́nà tó yẹ."},
        {"english": "The teacher asked us to revise because the test is tomorrow.",
         "yoruba": "Olùkọ́ ní ká tún ẹ̀kọ́ wò nítorí ìdánwò wà ní ọ̀la."},
        {"english": "When you finish the exercise, help your partner politely.",
         "yoruba": "Nígbà tí o bá parí ìdánilẹ́kọ̀ọ́ náà, ran alábàákẹ́gbẹ́ rẹ lọ́wọ́ pẹ̀lú ìwà rere."},
        {"english": "A school succeeds when teachers, students, and parents cooperate.",
         "yoruba": "Ilé ẹ̀kọ́ máa ń ṣàṣeyọrí nígbà tí olùkọ́, akẹ́kọ̀ọ́, àti òbí bá fọwọ́sowọ́pọ̀."},
        {"english": "The student was rewarded because she was honest.",
         "yoruba": "Wọ́n fún akẹ́kọ̀ọ́ náà ní ẹ̀bùn nítorí pé ó jẹ́ olóòtọ́."},
        {"english": "If the weather is fine, the students will play outside.",
         "yoruba": "Bí ojú ọjọ́ bá dára, àwọn akẹ́kọ̀ọ́ yóò ṣeré níta."},
        {"english": "We learn from our mistakes when we correct them.",
         "yoruba": "A máa ń kọ́ ẹ̀kọ́ lára àṣìṣe wa nígbà tí a bá ṣàtúnṣe wọn."},
    ],
}

# ================================================================
# DATASET UTILITIES
# ================================================================

def iter_examples(dataset=education_dataset):
    """Yield each English Yorùbá parallel example with its source section."""
    for section, examples in dataset.items():
        if isinstance(examples, list):
            for example in examples:
                if isinstance(example, dict) and {"english", "yoruba"} <= example.keys():
                    yield {"section": section, **example}


def dataset_summary(dataset=education_dataset):
    """Return the number of parallel examples in each dataset section."""
    return {
        section: len(examples)
        for section, examples in dataset.items()
        if isinstance(examples, list)
    }


def validate_dataset(dataset=education_dataset):
    """Report missing English or Yorùbá values without changing the data."""
    errors = []
    for index, example in enumerate(iter_examples(dataset), start=1):
        if not example["english"].strip() or not example["yoruba"].strip():
            errors.append(
                {"index": index, "section": example["section"], "error": "empty translation"}
            )
    return errors


def export_jsonl(path="yoruba_english_education_dataset.jsonl"):
    """Write the completed parallel dataset as UTF 8 JSONL."""
    import json

    with open(path, "w", encoding="utf-8") as file:
        for example in iter_examples():
            file.write(json.dumps(example, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    summary = dataset_summary()
    print("Yoruba English Education Dataset")
    print(f"Sections: {len(summary)}")
    print(f"Examples: {sum(summary.values())}")
    print(f"Validation errors: {len(validate_dataset())}")

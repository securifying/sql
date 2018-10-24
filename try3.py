from pymongo import MongoClient
import subprocess, os

client = MongoClient('localhost:27017')
db = client.latex

def main():

    while(1):
        selection = input('\n1. Insert\n2. Update\n3. Read\n4. Delete\n5. Generate\n6. Exit\n> ')
    
        if selection == '1':
            insert()
        elif selection == '2':
            update()
        elif selection == '3':
            read()
        elif selection == '4':
            delete()
        elif selection == '5':
            generate()
        elif selection == '6':
            exit()                        
        else:
            print ('INVALID SELECTION')


def insert():
    try:
        qId = input('Enter Question ID: ')
        qSubject = input('Enter Subject: ')
        qType = input('Enter type (Theory_1 / Theory_2 / MCQ): ')
        if qType == 'MCQ':
            insert_mcq(qId, qSubject)
        else:
            qText = input('Enter question text in LaTeX format: ')
            db.questions.insert_one(
                {
                "qId": qId,
                "qSubject":qSubject,
                "qType":qType,
                "qText":qText
                })
            print ('Inserted question successfully')
    except Exception as e:
        print(str(e))

def insert_mcq(qId, qSubject):
    try:
        qText = input('Enter question text in LaTeX format: ')
        n = int(input('How many options would you like to insert? '))
        options = []
        for x in range(1,n+1):
            options.append(input('Enter option #{}: '.format(x)))
        db.questions.insert_one(
            {
            "qId": qId,
            "qSubject":qSubject,
            "qType":"MCQ",
            "qText":qText,
            "qOptions":options
            })
        print ('Inserted question successfully')
    except Exception as e:
        print(str(e))        
    

def update():
    try:
        qId = input('Enter Question ID to update question: ')
        qSubject = input('Enter new Subject: ')
        qType = input('Enter new type (Theory_1 / Theory_2 / MCQ): ')
        qText = input('Enter new question text in LaTeX format: ')

        db.questions.update_one(
            {"qId": criteria},
            {
            "$set": {
            "qId": qId,
            "qSubject":qSubject,
            "qType":qType,
            "qText":qText
            }
            }
        )
        print ("Question updated successfully")    
    
    except Exception as e:
        print(str(e))

def read():
    try:
        qn = db.questions.find()
        print('\n All questions from question bank \n')
        for q in qn:
            print(q)

    except Exception as e:
        print(str(e))

def delete():
    try:
        criteria = input('\nEnter question qId to delete\n')
        db.questions.delete_many({"qId":criteria})
        print('\nDeletion successful\n') 
    except Exception as e:
        print(str(e))


def generate():
    try:
        header = (r"\documentclass{exam}"
        r"\usepackage{amsmath}"
        r"\usepackage{graphicx}"
        r"\usepackage{enumerate}"
        r"\usepackage{geometry}"
        r"\geometry{"
        r"a4paper,"
        r"total={170mm,240mm},"
        r"left=20mm,"
        r"top=20mm,"
        r"paperwidth=20cm,"
        r"paperheight=28cm"
        r"}"
        r"\usepackage[a4,frame,center]{crop}"
        r"\begin{document}"
        r"\begin{center}"
        r"\large{\textbf{Sample Question Paper using MongoDB}}"
        r"\end{center}"
        r"\begin{tabular}{p{13cm}r}"
        r"\textbf{Duration: 3 Hrs} & \textbf{30 marks}"
        r"\end{tabular}"
        r"\section{Answer all Questions. $4\times 1\frac{1}{2}$}"
        r"\begin{enumerate}")
        list_of_q = [header]
        tq = db.questions.find({"qType":"Theory_1"})
        for q in tq:
            list_of_q.append(q["qText"])

        mcqs = ()
            

        mcq_section = 
        final_body = ''.join(list_of_q)
        footer = (r"\end{enumerate}"
        r"\begin{center}\text{*** End ***}\end{center}"
        r"\end{document}")

        tex = final_body + footer

        f = open("paper.tex","w+")
        f.write(tex)
        f.close()
        cmd = "rubber --pdf paper.tex && xdg-open ./paper.pdf"
        os.system(cmd)

    except Exception as e:
        print(str(e))                    

main()

# import sys
# import os
# import tkinter as tk
# from tkinter import *
# import tkinter.messagebox

# # For Neo4j Connection
# from neo4j import GraphDatabase

# class Neo4jConnection:

#     def __init__(self, uri, user, pwd):
#         self.__uri = uri
#         self.__user = user
#         self.__pwd = pwd
#         self.__driver = None
#         try:
#             self.__driver = GraphDatabase.driver(
#                 self.__uri, auth=(self.__user, self.__pwd))
#         except Exception as e:
#             print("Failed to create the driver:", e)

#     def close(self):
#         if self.__driver is not None:
#             self.__driver.close()

#     def query(self, query, db=None):
#         assert self.__driver is not None, "Driver not initialized!"
#         session = None
#         response = None
#         try:
#             session = self.__driver.session(
#                 database=db) if db is not None else self.__driver.session()
#             response = list(session.run(query))
#         except Exception as e:
#             print("Query failed:", e)
#         finally:
#             if session is not None:
#                 session.close()
#         return response

# conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="neo4j")
# # ^ Neo4j Connected

# window = tk.Tk()
# window.title("Desktop App by Sagar")
# window.geometry("700x500")
# window.configure(bg="grey")
# blog = tk.StringVar()
# blog_title = tk.StringVar()
# direct_id1 = tk.StringVar()
# direct_id2 = tk.StringVar()
# recur_id1 = tk.StringVar()
# recur_id2 = tk.StringVar()

# # submitting query

# def submit():
#     query_string = blog_title.get()
#     result = conn.query(query_string, db='neo4j')
#     print(result)
#     blog.set("")

# def direct_check():
#     id1 = direct_id1.get()
#     id2 = direct_id2.get()
#     query_string = '''MATCH p=(:Paper{id:"'''+id1 + \
#         '''"})-[r:CITES]->(:Paper{id:"'''+id2+'''"}) RETURN p'''
#     result = conn.query(query_string, db='neo4j')
#     if (result):
#         Label(window, text="YES", fg="blue", font=(
#             "Arial", 15), width=37).grid(row=160)
#     else:
#         Label(window, text="NO", fg="RED", font=(
#             "Arial", 15), width=37).grid(row=160)
#     blog.set("")

# def indirect_check():
#     id1 = recur_id1.get()
#     id2 = recur_id2.get()
#     query_string = '''MATCH p=(:Paper{id:"'''+id1 + \ 
#     '''"})-[r:CITES]->() MATCH q=(:Paper{id:"'''+id2+'''"}) RETURN q'''
#     result = conn.query(query_string, db='neo4j')
#     if (result):
#           Label(window, text="YES", fg="blue", font=("Arial", 15), width=37).grid(row=220)
#     else:
#         Label(window, text="NO", fg="RED", font=(
#             "Arial", 15), width=37).grid(row=220)
#     blog.set("")

# # tkinter window
# Label(window, text="Neo4j Application", fg="black",
#       font=("Arial", 25, 'bold'), width=37).grid(row=0, column=0)
# name_label = tk.Label(window, text='Query', font=(
#     'calibre', 10, 'bold')).grid(row=70)
# name_entry = tk.Entry(window, textvariable=blog_title, font=(
#     'calibre', 10, 'normal'), width=70).grid(row=80)
# sub_btn = tk.Button(window, text='Run Query', command=submit).grid(row=110)

# name_label = tk.Label(window, text='Does Paper with id1 cites id2 directly?', font=(
#     'calibre', 10, 'bold')).grid(row=120)
# name_entry = tk.Entry(window, textvariable=direct_id1,
#                       font=('calibre', 10, 'normal')).grid(row=130)
# name_entry = tk.Entry(window, textvariable=direct_id2,
#                       font=('calibre', 10, 'normal')).grid(row=140)
# sub_btn = tk.Button(window, text='Check', command=direct_check).grid(row=150)

# name_label = tk.Label(window, text='Does Paper with id1 cites id2 indirectly?', font=(
#     'calibre', 10, 'bold')).grid(row=180)
# name_entry = tk.Entry(window, textvariable=recur_id1,
#                       font=('calibre', 10, 'normal')).grid(row=190)
# name_entry = tk.Entry(window, textvariable=recur_id2,
#                       font=('calibre', 10, 'normal')).grid(row=200)
# sub_btn = tk.Button(window, text='Check', command=indirect_check).grid(row=210)
	
# window.mainloop()
	

import tkinter as tk
from neo4j import GraphDatabase

# Neo4j database connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "root1234"

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to check if paper A cites paper B


def does_paper_a_cite_paper_b(tx, paper_a_id, paper_b_id):
    query = (
        "MATCH (a:Paper {paper_id: $paper_a_id})-[:CITATION*..3]->(b:Paper {paper_id: $paper_b_id}) "
        "RETURN count(*) > 0"
    )
    result = tx.run(query, paper_a_id=paper_a_id, paper_b_id=paper_b_id)
    return result.single()[0]

# Function to get the full classification of a paper


def get_classification_of_paper(tx, paper_id):
    query = (
        "MATCH (p:Paper {paper_id: $paper_id})-[:CLASSIFICATION*]->(c:Classification) "
        "RETURN c.name"
    )
    result = tx.run(query, paper_id=paper_id)
    return [record['c.name'] for record in result]

# Function to handle search button click


def search():
    # Get the paper IDs from the entry widgets
    paper_a_id = entry_paper_a_id.get()
    paper_b_id = entry_paper_b_id.get()
    paper_id = entry_paper_id.get()

    # Open a new Neo4j session
    with driver.session() as session:
        # Check if paper A cites paper B
        result_a_b = does_paper_a_cite_paper_b(session, paper_a_id, paper_b_id)
        label_a_b.config(text="Yes" if result_a_b else "No")

        # Check if paper A cites a paper that cites paper B
        result_a_cite_b = False
        for i in range(3):
            result_a_cite_b = does_paper_a_cite_paper_b(
                session, paper_a_id, paper_b_id)
            if result_a_cite_b:
                break
        label_a_cite_b.config(text="Yes" if result_a_cite_b else "No")

        # Get the full classification of the paper
        result_classification = get_classification_of_paper(session, paper_id)
        label_classification.config(text="/".join(result_classification))


# Create the main window
window = tk.Tk()
window.title("Research Papers Database")

# Create the widgets
label_paper_a_id = tk.Label(window, text="Paper A ID:")
entry_paper_a_id = tk.Entry(window)
label_paper_b_id = tk.Label(window, text="Paper B ID:")
entry_paper_b_id = tk.Entry(window)
button_search_citations = tk.Button(
    window, text="Search Citations", command=search)
label_a_b = tk.Label(window, text="")
label_a_cite_b = tk.Label(window, text="")
label_paper_id = tk.Label(window, text="Paper ID:")
entry_paper_id = tk.Entry(window)
button_search_classification = tk.Button(
    window, text="Search Classification", command=search)
label_classification = tk.Label(window, text="")

# Pack the widgets
label_paper_a_id.pack()
entry_paper_a_id.pack()
label_paper_b_id.pack()
entry_paper_b_id.pack()
button_search_citations.pack()
label_a_b.pack()
label_a_cite_b.pack()
label_paper_id.pack()
entry_paper_id.pack()
button_search_classification.pack()
label_classification.pack()

# Run the main loop
window.mainloop()

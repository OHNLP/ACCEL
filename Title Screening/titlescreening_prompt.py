#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#pip install openai


import pandas as pd
import os
import csv


# Load the CSV file
file_path = ''
df = pd.read_csv(file_path)

# Determine the number of splits based on chunks of 20 rows
num_chunks = len(df) // 50 + (1 if len(df) % 50 != 0 else 0)

# Iterate and save each chunk as a new CSV file
for i in range(num_chunks):
    chunk = df[i*50:(i+1)*50]
    output_path = f''
    chunk.to_csv(output_path, index=False)
    print(f'Saved: {output_path}')
    
    

# Define file paths
prompt_file = ''
csv_dir = ''
output_dir = ''

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the prompt from the prompt file
with open(prompt_file, 'r') as pf:
    prompt = pf.read().strip()

# Process each CSV file in the directory
for csv_file in os.listdir(csv_dir):
    if csv_file.endswith('.csv'):
        csv_path = os.path.join(csv_dir, csv_file)

        # Read the titles from the CSV file
        df = pd.read_csv(csv_path, header=None)  # Assuming no header
        titles = df.iloc[:, 0].tolist()  # Assuming titles are in the first column

        # Prepare the output content
        output_content = prompt + '\n\n' + '\n'.join(titles)

        # Write the output to a text file
        output_file = os.path.join(output_dir, f'{os.path.splitext(csv_file)[0]}.txt')
        with open(output_file, 'w') as of:
            of.write(output_content)

print("Files have been processed and saved to the output directory.")





from openai import OpenAI
client = OpenAI(api_key= "")


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "**Objective:**  \nYou will receive 23 article titles. For each title, determine if it is eligible based on the criteria below. Respond with only one word: \"eligible\" or \"ineligible,\" as a numbered list.\n\n**Eligibility Criteria:**  \nAn article is considered eligible if it meets both of the following criteria:\n\n1. The study is a randomized controlled trial (RCT). Acceptable terms include:  \n   - Randomised controlled trial, Randomized controlled study, Randomized trial, Randomized study, Randomized control trial, Randomized control study, Randomized clinical trial, Randomized clinical study.  \n   - Terms that describe specific types of RCT designs are also acceptable when used with RCTs: Parallel, parallel-group, non-inferiority, crossover, cross-over, factorial, pragmatic.\n\n2. The study involves the use of virtual reality (VR). VR includes any form of immersive digital environment that uses computer-generated simulations.\n\n**Exclusion Criteria:**  \nAn article is ineligible if it meets any of the following conditions:\n- The title includes terms like: \"Proof of concept,\" \"Feasibility,\" \"Preliminary efficacy,\" \"Pilot study,\" \"Protocol,\" \"First results,\" \"Preliminary results,\" \"Design,\" \"Economic evaluation,\" \"Health-economic evaluation,\" \"Secondary analysis,\" \"Qualitative study,\" \"Follow-up,\" \"Longitudinal study,\" \"Short term findings,\" \"Methods,\" \"Letter,\" \"Erratum,\" \"Commentary,\" \"Insights,\" \"Lessons learned,\" \"Reflections,\" \"Correlation study,\" \"Quasi,\" \"Survey,\" \"Process economic evaluation,\" \"Bibliometric analysis,\" \"Meta-analysis,\" \"Systematic review,\" \"Scoping review.\"  \n- The study does not explicitly state it is an RCT and does not involve VR.\n- The title is not written in English.\n-DO NOT include titles with the keyword secondary analysis.\n-DO NOT include titles with the keyword follow-up.\n\nNow, screen the following titles using the provided eligibility and exclusion criteria and respond with a numbered list selecting only \"eligible\" or \"ineligible\" for each title:\n\nComparison of virtual reality exercise versus conventional exercise on balance in patients with functional ankle instability: A randomized controlled trial\nNon-immersive Virtual Reality Rehabilitation Applied to a Task-oriented Approach for Stroke Patients: A Randomized Controlled Trial\nEnvironmental management education using immersive virtual reality in asthmatic children in Korea: a randomized controlled study (secondary publication)\n3D Virtual Reality Smartphone Training for Chemotherapy Drug Administration by Non-oncology Nurses: A Randomized Controlled Trial\nVirtual Reality Analgesia With Interactive Eye Tracking During Brief Thermal Pain Stimuli: A Randomized Controlled Trial (Crossover Design)\nFeasibility of hemispatial neglect rehabilitation with virtual reality-based visual exploration therapy among patients with stroke: randomised controlled trial\nUsing Virtual Reality to Assess and Promote Transfer of Memory Training in Older Adults With Memory Complaints: A Randomized Controlled Trial\nThe efficacy of virtual reality exposure therapy for the treatment of alcohol use disorder among adult males: a randomized controlled trial comparing with acceptance and commitment therapy and treatment as usual\nEffects of Specific Virtual Reality-Based Therapy for the Rehabilitation of the Upper Limb Motor Function Post-Ictus: Randomized Controlled Trial\nEfficacy of the Virtual Reality Intervention VR FestLab on Alcohol Refusal Self-Efficacy: A Cluster-Randomized Controlled Trial\nThe Level of Surface Coverage of Surgical Site Disinfection Depends on the Visibility of the Antiseptic Agent-A Virtual Reality Randomized Controlled Trial\nVirtual Reality Distraction during Endoscopic Urologic Surgery under Spinal Anesthesia: A Randomized Controlled Trial\nAnalysis of Usage Data from a Self-Guided App-Based Virtual Reality Cognitive Behavior Therapy for Acrophobia: A Randomized Controlled Trial\nEffectiveness of Virtual Reality-Based Training on Oral Healthcare for Disabled Elderly Persons: A Randomized Controlled Trial\nA Randomized Controlled Trial of Motor Imagery Combined with Virtual Reality Techniques in Patients with Parkinson's Disease\nUsing Virtual Reality in the Care of Older Adults With Dementia: A Randomized Controlled Trial\nThe Use of Virtual Reality to Improve Disaster Preparedness Among Nursing Students: A Randomized Study\nVirtual Reality Game Playing in Amblyopia Therapy: A Randomized Clinical Trial\nCombined Effect of Virtual Reality Training (VRT) and Conventional Therapy on Sitting Balance in Patients with Spinal Cord Injury (SCI): Randomized Control Trial\nVirtual reality mobile application to improve videoscopic airway training: A randomised trial\nVirtual Reality as a Learning Tool for Trainees in Unicompartmental Knee Arthroplasty: A Randomized Controlled Trial\nA Virtual Reality Game for Chronic Pain Management: A Randomized, Controlled Clinical Study\nVirtual reality in cardiopulmonary resuscitation training: a randomized trial"
                }
            ]
        }
    ],
    temperature=0.25,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
)

# Extract response text and split into a list
response_text = response.choices[0].message.content.strip()
response_list = response_text.split("\n")

# Save responses to CSV
csv_filename = ""

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Article Number", "Eligibility"])

    for line in response_list:
        if line.strip():
            parts = line.split(". ")
            if len(parts) == 2:
                article_number = parts[0]
                eligibility = parts[1]
                writer.writerow([article_number, eligibility])

print(f"Responses saved to {csv_filename}")

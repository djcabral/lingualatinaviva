import json
import os

def generate_grok_prompt():
    # Source files
    sentences_path = "data/sentences_for_ai_analysis.json"
    prompt_template_path = "data/ai_analysis_prompt.md"
    output_path = "data/grok_reboot_prompt.md"
    
    # Ranges to extract
    # Batch 3 remainder: 265-360
    # Batch 5: 481-end (482)
    
    with open(sentences_path, 'r') as f:
        data = json.load(f)
        all_sentences = data["sentences"]
    
    missing_sentences = []
    for s in all_sentences:
        sid = s["id"]
        if (265 <= sid <= 360) or (sid >= 481):
            missing_sentences.append(s)
            
    print(f"Found {len(missing_sentences)} missing sentences to process.")
    ids = sorted([s["id"] for s in missing_sentences])
    if ids:
        print(f"ID Range: {ids[0]} - {ids[-1]}")
        # Detect gaps
        gaps = []
        for i in range(1, len(ids)):
            if ids[i] > ids[i-1] + 1:
                gaps.append(f"{ids[i-1]}->{ids[i]}")
        if gaps:
            print(f"Gaps found: {gaps}")
        else:
            print("No gaps found in result.")
    
    # Load prompt template
    with open(prompt_template_path, 'r') as f:
        prompt_content = f.read()
        
    # Append the specific sentences
    full_content = prompt_content + "\n\n# INPUT DATA (Remaining Batches)\n\n```json\n" + json.dumps(missing_sentences, indent=2, ensure_ascii=False) + "\n```"
    
    with open(output_path, 'w') as f:
        f.write(full_content)
        
    print(f"✅ Generated {output_path} with instructions and {len(missing_sentences)} sentences.")

if __name__ == "__main__":
    generate_grok_prompt()

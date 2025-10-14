import anthropic
import os
from typing import List, Dict, Any
import json

class CaseComparisonService:
    """Service for comparing legal cases using Claude API"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.model = "claude-sonnet-4-5-20250929"
    
    def compare_cases(self, new_case: Dict[str, Any], previous_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare a new case with previous cases to find similarities and differences
        
        Args:
            new_case: Dictionary containing new case details
            previous_cases: List of dictionaries containing previous case details
        
        Returns:
            Dictionary containing comparison results
        """
        
        # Prepare the prompt
        prompt = self._build_comparison_prompt(new_case, previous_cases)
        
        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            response_text = message.content[0].text
            
            return {
                'success': True,
                'analysis': response_text,
                'similar_cases': self._extract_similar_cases(response_text, previous_cases),
                'key_differences': self._extract_differences(response_text),
                'recommendations': self._extract_recommendations(response_text)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }
    
    def _build_comparison_prompt(self, new_case: Dict[str, Any], previous_cases: List[Dict[str, Any]]) -> str:
        """Build the prompt for Claude"""
        
        prompt = f"""You are a legal expert analyzing case similarities and differences. 

NEW CASE:
Case ID: {new_case.get('id', 'N/A')}
Title: {new_case.get('title', 'N/A')}
Type: {new_case.get('type', 'N/A')}
Description: {new_case.get('description', 'N/A')}
Client: {new_case.get('client', 'N/A')}
Key Facts: {new_case.get('key_facts', 'N/A')}
Legal Issues: {new_case.get('legal_issues', 'N/A')}

PREVIOUS CASES TO COMPARE:
"""
        
        for i, case in enumerate(previous_cases, 1):
            prompt += f"""
Case {i}:
- ID: {case.get('id', 'N/A')}
- Title: {case.get('title', 'N/A')}
- Type: {case.get('type', 'N/A')}
- Description: {case.get('description', 'N/A')}
- Outcome: {case.get('outcome', 'N/A')}
- Key Facts: {case.get('key_facts', 'N/A')}
- Legal Issues: {case.get('legal_issues', 'N/A')}
---
"""
        
        prompt += """
Please provide a comprehensive analysis including:

1. **SIMILARITY ANALYSIS**
   - Identify which previous cases are most similar to the new case
   - Rank them by similarity (1-10 scale)
   - Explain the key similarities (legal issues, facts, client type, etc.)

2. **KEY DIFFERENCES**
   - Highlight important differences between the new case and similar previous cases
   - Note any unique aspects of the new case

3. **PRECEDENT VALUE**
   - Which previous cases provide the most relevant precedent?
   - What outcomes or strategies from previous cases are applicable?

4. **RISK ASSESSMENT**
   - Based on previous case outcomes, what are the potential risks?
   - What factors might lead to different outcomes?

5. **STRATEGIC RECOMMENDATIONS**
   - What strategies worked well in similar previous cases?
   - What approaches should be avoided based on past experience?
   - Specific action items for this new case

6. **RESOURCE ALLOCATION**
   - Estimated complexity compared to similar cases
   - Suggested team composition based on previous cases
   - Time and cost estimates

Format your response in clear sections with bullet points for easy reading.
"""
        
        return prompt
    
    def _extract_similar_cases(self, analysis: str, previous_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract similar cases mentioned in the analysis"""
        similar = []
        
        for case in previous_cases:
            case_id = case.get('id', '')
            case_title = case.get('title', '')
            
            # Simple extraction - check if case is mentioned in analysis
            if case_id in analysis or case_title.lower() in analysis.lower():
                similar.append({
                    'case_id': case_id,
                    'title': case_title,
                    'type': case.get('type', 'N/A')
                })
        
        return similar
    
    def _extract_differences(self, analysis: str) -> List[str]:
        """Extract key differences from the analysis"""
        # Look for the differences section
        differences = []
        
        if "KEY DIFFERENCES" in analysis:
            section = analysis.split("KEY DIFFERENCES")[1].split("PRECEDENT VALUE")[0] if "PRECEDENT VALUE" in analysis else analysis.split("KEY DIFFERENCES")[1]
            
            # Extract bullet points
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    differences.append(line.lstrip('-•* '))
        
        return differences[:5]  # Return top 5
    
    def _extract_recommendations(self, analysis: str) -> List[str]:
        """Extract strategic recommendations from the analysis"""
        recommendations = []
        
        if "STRATEGIC RECOMMENDATIONS" in analysis:
            section = analysis.split("STRATEGIC RECOMMENDATIONS")[1].split("RESOURCE ALLOCATION")[0] if "RESOURCE ALLOCATION" in analysis else analysis.split("STRATEGIC RECOMMENDATIONS")[1]
            
            # Extract bullet points
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    recommendations.append(line.lstrip('-•* '))
        
        return recommendations[:5]  # Return top 5
    
    def quick_similarity_score(self, case1: Dict[str, Any], case2: Dict[str, Any]) -> float:
        """
        Quick similarity score between two cases using Claude
        Returns a score between 0 and 1
        """
        
        prompt = f"""Compare these two legal cases and provide a similarity score from 0 to 1.

CASE 1:
{json.dumps(case1, indent=2)}

CASE 2:
{json.dumps(case2, indent=2)}

Respond with ONLY a number between 0 and 1, where:
- 0 = completely different
- 0.5 = moderately similar
- 1 = nearly identical

Consider: case type, legal issues, facts, parties involved, and outcomes.
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            score_text = message.content[0].text.strip()
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            
        except:
            return 0.0

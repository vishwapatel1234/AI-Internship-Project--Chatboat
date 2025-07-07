import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

class MedicalUtils:
    """Utility class for medical-related functions"""
    
    def __init__(self):
        self.emergency_keywords = [
            "chest pain", "can't breathe", "difficulty breathing", "severe bleeding",
            "stroke", "heart attack", "suicide", "kill myself", "overdose",
            "severe headache", "unconscious", "seizure", "choking", "allergic reaction",
            "severe abdominal pain", "high fever", "severe burn", "broken bone"
        ]
        
        self.urgent_keywords = [
            "high fever", "severe pain", "vomiting blood", "difficulty swallowing",
            "sudden dizziness", "severe allergic reaction", "persistent vomiting",
            "severe dehydration", "rapid heart rate", "confusion"
        ]
        
        self.common_symptoms = {
            "fever": {
                "description": "Elevated body temperature above 100.4°F (38°C)",
                "when_to_seek_care": "If fever is above 103°F, lasts more than 3 days, or accompanied by severe symptoms"
            },
            "headache": {
                "description": "Pain in the head or upper neck",
                "when_to_seek_care": "If sudden, severe, or accompanied by neck stiffness, vision changes, or confusion"
            },
            "cough": {
                "description": "Forceful expulsion of air from lungs",
                "when_to_seek_care": "If persistent for more than 2 weeks, producing blood, or with difficulty breathing"
            },
            "sore throat": {
                "description": "Pain or irritation in the throat",
                "when_to_seek_care": "If severe, lasting more than a week, or with high fever"
            }
        }
    
    def assess_urgency(self, message: str) -> Tuple[str, str]:
        """
        Assess the urgency level of a medical message
        Returns: (urgency_level, explanation)
        """
        message_lower = message.lower()
        
        # Check for emergency keywords
        if any(keyword in message_lower for keyword in self.emergency_keywords):
            return ("EMERGENCY", "This appears to be a medical emergency. Seek immediate medical attention.")
        
        # Check for urgent keywords
        if any(keyword in message_lower for keyword in self.urgent_keywords):
            return ("URGENT", "This may require prompt medical attention. Consider contacting a healthcare provider.")
        
        # Check for concerning patterns
        if self._check_concerning_patterns(message_lower):
            return ("MODERATE", "This should be evaluated by a healthcare provider if symptoms persist.")
        
        return ("LOW", "This appears to be a general health inquiry.")
    
    def _check_concerning_patterns(self, message: str) -> bool:
        """Check for concerning symptom patterns"""
        concerning_patterns = [
            r"pain.*(\d+|ten|severe|unbearable)",
            r"bleeding.*(\d+|hours|days)",
            r"fever.*(\d+|high|very)",
            r"can't.*sleep.*(\d+|days|weeks)",
            r"lost.*weight.*(\d+|pounds|kg)",
        ]
        
        return any(re.search(pattern, message) for pattern in concerning_patterns)
    
    def get_symptom_info(self, symptom: str) -> Optional[Dict]:
        """Get information about a common symptom"""
        symptom_lower = symptom.lower()
        for key, info in self.common_symptoms.items():
            if key in symptom_lower:
                return info
        return None
    
    def calculate_bmi(self, weight_kg: float, height_m: float) -> Dict:
        """Calculate BMI and provide interpretation"""
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
            advice = "Consider consulting with a healthcare provider about healthy weight gain."
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            advice = "Maintain your current healthy lifestyle."
        elif 25 <= bmi < 30:
            category = "Overweight"
            advice = "Consider lifestyle changes including diet and exercise. Consult a healthcare provider."
        else:
            category = "Obese"
            advice = "Strongly recommend consulting with a healthcare provider for a comprehensive health plan."
        
        return {
            "bmi": round(bmi, 1),
            "category": category,
            "advice": advice
        }
    
    def medication_interaction_check(self, medications: List[str]) -> Dict:
        """Basic medication interaction checker (simplified)"""
        # This is a simplified version - in reality, you'd use a proper drug database
        known_interactions = {
            ("warfarin", "aspirin"): "Increased bleeding risk",
            ("warfarin", "ibuprofen"): "Increased bleeding risk",
            ("metformin", "alcohol"): "Risk of lactic acidosis",
            ("statins", "grapefruit"): "Increased statin levels"
        }
        
        interactions = []
        medications_lower = [med.lower() for med in medications]
        
        for i, med1 in enumerate(medications_lower):
            for med2 in medications_lower[i+1:]:
                interaction_key = tuple(sorted([med1, med2]))
                if interaction_key in known_interactions:
                    interactions.append({
                        "medications": [med1, med2],
                        "interaction": known_interactions[interaction_key]
                    })
        
        return {
            "has_interactions": len(interactions) > 0,
            "interactions": interactions,
            "disclaimer": "This is a basic check. Always consult your pharmacist or doctor for comprehensive interaction screening."
        }
    
    def generate_health_tips(self, age: int, gender: str) -> List[str]:
        """Generate age and gender-appropriate health tips"""
        tips = [
            "Stay hydrated by drinking plenty of water throughout the day",
            "Aim for 7-9 hours of quality sleep each night",
            "Eat a balanced diet rich in fruits, vegetables, and whole grains",
            "Exercise regularly - aim for at least 150 minutes of moderate activity per week"
        ]
        
        # Age-specific tips
        if age < 18:
            tips.extend([
                "Ensure you're getting enough calcium and vitamin D for bone development",
                "Limit screen time and take regular breaks from devices"
            ])
        elif 18 <= age < 40:
            tips.extend([
                "Establish healthy habits now to prevent chronic diseases later",
                "Consider regular health screenings as recommended by your doctor"
            ])
        elif 40 <= age < 65:
            tips.extend([
                "Schedule regular screenings for blood pressure, cholesterol, and diabetes",
                "Consider bone density testing if at risk for osteoporosis"
            ])
        else:
            tips.extend([
                "Focus on fall prevention and balance exercises",
                "Ensure you're up to date with vaccinations including flu and pneumonia"
            ])
        
        # Gender-specific tips
        if gender.lower() == "female":
            tips.extend([
                "Don't forget regular mammograms and cervical cancer screenings",
                "Ensure adequate iron intake, especially if menstruating"
            ])
        elif gender.lower() == "male":
            tips.extend([
                "Consider regular prostate health screenings after age 50",
                "Be aware of heart disease risk factors"
            ])
        
        return tips
    
    def create_symptom_tracker(self) -> Dict:
        """Create a basic symptom tracking template"""
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "symptoms": [],
            "severity": None,  # 1-10 scale
            "duration": None,
            "triggers": [],
            "treatments_tried": [],
            "notes": ""
        }
    
    def validate_vital_signs(self, vitals: Dict) -> Dict:
        """Validate and interpret vital signs"""
        results = {}
        
        # Blood pressure
        if "systolic" in vitals and "diastolic" in vitals:
            systolic = vitals["systolic"]
            diastolic = vitals["diastolic"]
            
            if systolic < 90 or diastolic < 60:
                bp_status = "Low (Hypotension)"
            elif systolic < 120 and diastolic < 80:
                bp_status = "Normal"
            elif systolic < 130 and diastolic < 80:
                bp_status = "Elevated"
            elif systolic < 140 or diastolic < 90:
                bp_status = "High Blood Pressure Stage 1"
            elif systolic < 180 or diastolic < 120:
                bp_status = "High Blood Pressure Stage 2"
            else:
                bp_status = "Hypertensive Crisis - Seek immediate care"
            
            results["blood_pressure"] = {
                "reading": f"{systolic}/{diastolic}",
                "status": bp_status
            }
        
        # Heart rate
        if "heart_rate" in vitals:
            hr = vitals["heart_rate"]
            if hr < 60:
                hr_status = "Low (Bradycardia)"
            elif hr <= 100:
                hr_status = "Normal"
            else:
                hr_status = "High (Tachycardia)"
            
            results["heart_rate"] = {
                "reading": f"{hr} bpm",
                "status": hr_status
            }
        
        # Temperature
        if "temperature" in vitals:
            temp = vitals["temperature"]
            temp_unit = vitals.get("temp_unit", "F")
            
            if temp_unit.upper() == "F":
                if temp < 97:
                    temp_status = "Low"
                elif temp <= 99.5:
                    temp_status = "Normal"
                elif temp <= 100.3:
                    temp_status = "Low-grade fever"
                elif temp <= 102:
                    temp_status = "Moderate fever"
                else:
                    temp_status = "High fever - seek medical attention"
            else:  # Celsius
                if temp < 36.1:
                    temp_status = "Low"
                elif temp <= 37.5:
                    temp_status = "Normal"
                elif temp <= 37.9:
                    temp_status = "Low-grade fever"
                elif temp <= 38.9:
                    temp_status = "Moderate fever"
                else:
                    temp_status = "High fever - seek medical attention"
            
            results["temperature"] = {
                "reading": f"{temp}°{temp_unit}",
                "status": temp_status
            }
        
        return results
    
    def get_medication_reminders(self, medications: List[Dict]) -> List[Dict]:
        """Generate medication reminders"""
        reminders = []
        current_time = datetime.now()
        
        for med in medications:
            if "schedule" in med and "last_taken" in med:
                last_taken = datetime.fromisoformat(med["last_taken"])
                interval_hours = med.get("interval_hours", 24)
                next_dose = last_taken + timedelta(hours=interval_hours)
                
                if next_dose <= current_time:
                    reminders.append({
                        "medication": med["name"],
                        "due_time": next_dose.strftime("%H:%M"),
                        "overdue": True if current_time - next_dose > timedelta(hours=1) else False
                    })
        
        return reminders
    
    def format_health_summary(self, user_profile: Dict, recent_symptoms: List[Dict]) -> str:
        """Format a health summary for the user"""
        summary = "## Your Health Summary\n\n"
        
        # Basic info
        if user_profile.get("age"):
            summary += f"**Age:** {user_profile['age']}\n"
        if user_profile.get("gender"):
            summary += f"**Gender:** {user_profile['gender']}\n"
        
        # Medical conditions
        if user_profile.get("medical_conditions"):
            summary += f"**Medical Conditions:** {', '.join(user_profile['medical_conditions'])}\n"
        
        # Allergies
        if user_profile.get("allergies"):
            summary += f"**Allergies:** {', '.join(user_profile['allergies'])}\n"
        
        # Recent symptoms
        if recent_symptoms:
            summary += "\n**Recent Symptoms:**\n"
            for symptom in recent_symptoms[-5:]:  # Last 5 symptoms
                summary += f"- {symptom.get('date', 'Unknown date')}: {symptom.get('description', 'No description')}\n"
        
        # Health tips
        if user_profile.get("age") and user_profile.get("gender"):
            tips = self.generate_health_tips(user_profile["age"], user_profile["gender"])
            summary += "\n**Personalized Health Tips:**\n"
            for tip in tips[:3]:  # Top 3 tips
                summary += f"- {tip}\n"
        
        summary += "\n*Remember: This summary is for informational purposes only. Always consult with healthcare professionals for medical advice.*"
        
        return summary


class DrugDatabase:
    """Simplified drug information database"""
    
    def __init__(self):
        self.drugs = {
            "acetaminophen": {
                "generic_name": "Acetaminophen",
                "brand_names": ["Tylenol", "Panadol"],
                "category": "Pain reliever/Fever reducer",
                "common_uses": ["Pain relief", "Fever reduction"],
                "max_daily_dose": "4000mg for adults",
                "warnings": ["Do not exceed maximum dose", "Avoid alcohol", "Check other medications for acetaminophen content"],
                "side_effects": ["Rare at normal doses", "Liver damage with overdose"]
            },
            "ibuprofen": {
                "generic_name": "Ibuprofen",
                "brand_names": ["Advil", "Motrin"],
                "category": "NSAID (Non-steroidal anti-inflammatory drug)",
                "common_uses": ["Pain relief", "Inflammation reduction", "Fever reduction"],
                "max_daily_dose": "1200mg for adults (OTC), up to 3200mg (prescription)",
                "warnings": ["Take with food", "Avoid if history of stomach ulcers", "May increase bleeding risk"],
                "side_effects": ["Stomach upset", "Heartburn", "Dizziness", "Increased bleeding risk"]
            },
            "aspirin": {
                "generic_name": "Aspirin",
                "brand_names": ["Bayer", "Bufferin"],
                "category": "NSAID/Antiplatelet",
                "common_uses": ["Pain relief", "Heart attack prevention", "Stroke prevention"],
                "max_daily_dose": "Varies by indication (81mg-4000mg)",
                "warnings": ["Increased bleeding risk", "Not for children with viral infections", "Take with food"],
                "side_effects": ["Stomach irritation", "Increased bleeding", "Ringing in ears (high doses)"]
            }
        }
    
    def get_drug_info(self, drug_name: str) -> Optional[Dict]:
        """Get information about a specific drug"""
        drug_name_lower = drug_name.lower()
        
        # Direct match
        if drug_name_lower in self.drugs:
            return self.drugs[drug_name_lower]
        
        # Check brand names
        for generic, info in self.drugs.items():
            brand_names_lower = [brand.lower() for brand in info["brand_names"]]
            if drug_name_lower in brand_names_lower:
                return info
        
        return None
    
    def search_drugs(self, query: str) -> List[Dict]:
        """Search for drugs matching a query"""
        results = []
        query_lower = query.lower()
        
        for generic, info in self.drugs.items():
            # Check generic name
            if query_lower in generic:
                results.append({"name": generic, "info": info})
                continue
            
            # Check brand names
            for brand in info["brand_names"]:
                if query_lower in brand.lower():
                    results.append({"name": generic, "info": info})
                    break
            
            # Check uses
            for use in info["common_uses"]:
                if query_lower in use.lower():
                    results.append({"name": generic, "info": info})
                    break
        
        return results


class HealthAssessment:
    """Health assessment and risk evaluation tools"""
    
    def __init__(self):
        self.risk_factors = {
            "cardiovascular": [
                "smoking", "high_blood_pressure", "high_cholesterol", 
                "diabetes", "family_history", "obesity", "sedentary_lifestyle"
            ],
            "diabetes": [
                "obesity", "family_history", "high_blood_pressure",
                "sedentary_lifestyle", "age_over_45", "gestational_diabetes"
            ],
            "osteoporosis": [
                "female", "age_over_50", "smoking", "low_calcium",
                "sedentary_lifestyle", "family_history", "thin_build"
            ]
        }
    
    def assess_cardiovascular_risk(self, risk_factors: List[str], age: int) -> Dict:
        """Assess cardiovascular disease risk"""
        applicable_factors = [
            factor for factor in risk_factors 
            if factor in self.risk_factors["cardiovascular"]
        ]
        
        risk_score = len(applicable_factors)
        
        # Age factor
        if age > 65:
            risk_score += 2
        elif age > 45:
            risk_score += 1
        
        if risk_score == 0:
            risk_level = "Low"
            recommendations = ["Maintain healthy lifestyle", "Regular check-ups"]
        elif risk_score <= 2:
            risk_level = "Moderate"
            recommendations = [
                "Focus on modifiable risk factors",
                "Regular blood pressure and cholesterol checks",
                "Consider lifestyle modifications"
            ]
        else:
            risk_level = "High"
            recommendations = [
                "Consult with healthcare provider immediately",
                "Comprehensive cardiovascular evaluation needed",
                "Aggressive lifestyle modifications required"
            ]
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "applicable_factors": applicable_factors,
            "recommendations": recommendations
        }
    
    def create_health_action_plan(self, assessment_results: Dict) -> List[str]:
        """Create a personalized health action plan"""
        action_items = []
        
        # Based on risk assessments
        if assessment_results.get("cardiovascular_risk", {}).get("risk_level") in ["Moderate", "High"]:
            action_items.extend([
                "Schedule appointment with primary care physician",
                "Begin or increase cardiovascular exercise (with doctor approval)",
                "Implement heart-healthy diet changes"
            ])
        
        # General health actions
        action_items.extend([
            "Establish regular sleep schedule (7-9 hours)",
            "Stay hydrated throughout the day",
            "Practice stress management techniques",
            "Schedule regular preventive health screenings"
        ])
        
        return action_items[:8]  # Limit to 8 actionable items
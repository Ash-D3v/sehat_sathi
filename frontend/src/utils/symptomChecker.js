import { SYMPTOMS_DATABASE, DISEASES_DATABASE, HOSPITALS_DATABASE, DOCTORS_DATABASE } from '../data/mockData.js';

export class SymptomChecker {
  constructor() {
    this.symptoms = SYMPTOMS_DATABASE;
    this.diseases = DISEASES_DATABASE;
    this.hospitals = HOSPITALS_DATABASE;
    this.doctors = DOCTORS_DATABASE;
  }

  // Analyze user input and extract symptoms
  analyzeSymptoms(userInput) {
    const input = userInput.toLowerCase();
    const detectedSymptoms = [];
    
    // Check for symptom keywords in user input
    Object.keys(this.symptoms).forEach(symptom => {
      if (input.includes(symptom) || this.checkSynonyms(input, symptom)) {
        detectedSymptoms.push(symptom);
      }
    });

    return detectedSymptoms;
  }

  // Check for symptom synonyms
  checkSynonyms(input, symptom) {
    const synonyms = {
      'stomach pain': ['belly ache', 'abdominal pain', 'tummy ache'],
      'headache': ['head pain', 'head ache'],
      'shortness of breath': ['breathing difficulty', 'cant breathe', 'breathless'],
      'chest pain': ['chest ache', 'heart pain'],
      'body ache': ['body pain', 'muscle pain', 'joint pain'],
      'sore throat': ['throat pain', 'throat ache']
    };

    if (synonyms[symptom]) {
      return synonyms[symptom].some(synonym => input.includes(synonym));
    }
    return false;
  }

  // Predict possible diseases based on symptoms
  predictDiseases(symptoms) {
    const diseaseScores = {};
    
    symptoms.forEach(symptom => {
      const possibleDiseases = this.symptoms[symptom] || [];
      possibleDiseases.forEach(disease => {
        diseaseScores[disease] = (diseaseScores[disease] || 0) + 1;
      });
    });

    // Sort diseases by score (number of matching symptoms)
    const sortedDiseases = Object.entries(diseaseScores)
      .sort(([,a], [,b]) => b - a)
      .map(([disease, score]) => ({
        name: disease,
        score,
        confidence: Math.min((score / symptoms.length) * 100, 95),
        ...this.diseases[disease]
      }));

    return sortedDiseases;
  }

  // Get recommendations based on disease severity
  getRecommendations(disease) {
    const recommendations = {
      treatment: disease.treatment,
      duration: disease.duration,
      urgency: disease.urgency
    };

    switch (disease.severity) {
      case 'low':
        recommendations.action = 'Self-care at home';
        recommendations.message = 'This condition can usually be managed at home with proper care.';
        recommendations.hospitals = [];
        recommendations.doctors = this.doctors.filter(doc => 
          doc.specialty === 'General Medicine'
        ).slice(0, 2);
        break;

      case 'medium':
        recommendations.action = 'Consult a doctor';
        recommendations.message = 'Please schedule an appointment with a healthcare provider within 24-48 hours.';
        recommendations.hospitals = this.hospitals.filter(h => !h.emergency).slice(0, 2);
        recommendations.doctors = this.doctors.filter(doc => 
          doc.specialty === 'General Medicine' || doc.specialty === 'Internal Medicine'
        ).slice(0, 2);
        break;

      case 'high':
        recommendations.action = 'Seek immediate medical attention';
        recommendations.message = 'Please visit a hospital or emergency room as soon as possible.';
        recommendations.hospitals = this.hospitals.filter(h => h.emergency).slice(0, 3);
        recommendations.doctors = this.doctors.filter(doc => 
          doc.specialty === 'Emergency Medicine' || doc.specialty.includes(disease.name.split(' ')[0])
        ).slice(0, 2);
        break;

      case 'critical':
        recommendations.action = 'EMERGENCY - Call 108 immediately';
        recommendations.message = '🚨 This is a medical emergency! Call an ambulance immediately or go to the nearest emergency room.';
        recommendations.hospitals = this.hospitals.filter(h => h.emergency);
        recommendations.doctors = this.doctors.filter(doc => 
          doc.specialty === 'Emergency Medicine' || doc.availability.includes('24/7')
        );
        break;

      default:
        recommendations.action = 'Consult a healthcare provider';
        recommendations.message = 'Please consult with a medical professional for proper diagnosis.';
        recommendations.hospitals = this.hospitals.slice(0, 2);
        recommendations.doctors = this.doctors.slice(0, 2);
    }

    return recommendations;
  }

  // Main function to process user input and return complete analysis
  processSymptoms(userInput) {
    const detectedSymptoms = this.analyzeSymptoms(userInput);
    
    if (detectedSymptoms.length === 0) {
      return {
        hasSymptoms: false,
        message: "I couldn't detect any specific symptoms in your message. Could you please describe what you're feeling more specifically?",
        suggestions: [
          "Try describing symptoms like: headache, fever, stomach pain, cough, etc.",
          "Be specific about the location and intensity of pain",
          "Mention how long you've been experiencing these symptoms"
        ]
      };
    }

    const predictedDiseases = this.predictDiseases(detectedSymptoms);
    const topDisease = predictedDiseases[0];
    const recommendations = this.getRecommendations(topDisease);

    return {
      hasSymptoms: true,
      detectedSymptoms,
      predictedDiseases: predictedDiseases.slice(0, 3), // Top 3 predictions
      topDisease,
      recommendations,
      severity: topDisease.severity,
      confidence: topDisease.confidence
    };
  }

  // Generate map URL for hospital location
  generateMapUrl(hospital) {
    const { lat, lng } = hospital.coordinates;
    return `https://www.google.com/maps/search/?api=1&query=${lat},${lng}&query_place_id=${hospital.name}`;
  }

  // Get emergency contacts
  getEmergencyContacts() {
    return {
      ambulance: '108',
      police: '100',
      fire: '101',
      women_helpline: '1091'
    };
  }
}

export default SymptomChecker;
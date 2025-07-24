import React, { useState, useEffect, useRef } from 'react';
import styles from '../styles/LandingPage.module.css';
import { useNavigate } from 'react-router-dom';
const LandingPage = () => {
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showTutorial, setShowTutorial] = useState(false);
  const [currentTip, setCurrentTip] = useState(0);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const heroRef = useRef(null);
  const navigate = useNavigate();


  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // PWA Install Prompt Handler
  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowInstallPrompt(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    
    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  // Tutorial tips rotation
  const tutorialTips = {
    en: [
      "💬 Simply describe how you're feeling",
      "🎤 Use voice input for hands-free interaction",
      "🗺️ Get directions to nearby healthcare facilities",
      "📱 Works offline with basic features",
      "🔒 Your privacy is completely protected"
    ],
    hi: [
      "💬 बस बताएं कि आप कैसा महसूस कर रहे हैं",
      "🎤 हाथों से मुक्त बातचीत के लिए वॉइस इनपुट का उपयोग करें",
      "🗺️ नजदीकी स्वास्थ्य सुविधाओं के दिशा-निर्देश प्राप्त करें",
      "📱 बुनियादी सुविधाओं के साथ ऑफलाइन काम करता है",
      "🔒 आपकी गोपनीयता पूरी तरह सुरक्षित है"
    ]
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTip((prev) => (prev + 1) % tutorialTips[selectedLanguage].length);
    }, 3000);
    return () => clearInterval(interval);
  }, [selectedLanguage]);

  const handleInstallClick = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      setDeferredPrompt(null);
      setShowInstallPrompt(false);
    }
  };

  const languages = {
    en: { name: 'English', flag: '🇺🇸' },
    hi: { name: 'हिंदी', flag: '🇮🇳' },
    es: { name: 'Español', flag: '🇪🇸' },
    fr: { name: 'Français', flag: '🇫🇷' },
    ar: { name: 'العربية', flag: '🇸🇦' }
  };

  const translations = {
    en: {
      title: 'SehatSathi',
      tagline: 'Your AI Health Companion',
      subtitle: 'Bridging Healthcare Gaps in Rural Communities',
      description: 'Experience instant medical consultation powered by advanced AI. Get personalized health advice, symptom analysis, and connect with nearby healthcare providers - all from your mobile device.',
      startChat: 'Start Health Consultation',
      emergencyCall: 'Emergency Services',
      howItWorks: 'How It Works',
      features: {
        instant: 'Instant AI Analysis',
        available: '24/7 Availability',
        secure: 'Bank-Level Security',
        offline: 'Works Offline',
        multilingual: 'Multi-Language',
        referral: 'Smart Referrals'
      },
      stats: {
        consultations: '50K+ Consultations',
        users: '15K+ Active Users',
        accuracy: '94% Accuracy Rate',
        languages: '5+ Languages'
      },
      privacy: 'Your health data remains private and encrypted',
      tutorial: 'Describe your symptoms naturally - we understand',
      steps: [
        'Describe your symptoms in plain language',
        'Get instant AI-powered health analysis',
        'Receive personalized care recommendations',
        'Connect with nearby healthcare providers'
      ]
    },
    hi: {
      title: 'सेहतसाथी',
      tagline: 'आपका AI स्वास्थ्य साथी',
      subtitle: 'ग्रामीण समुदायों में स्वास्थ्य सेवा की कमी को पाटना',
      description: 'उन्नत AI द्वारा संचालित तत्काल चिकित्सा परामर्श का अनुभव करें। व्यक्तिगत स्वास्थ्य सलाह, लक्षण विश्लेषण प्राप्त करें और नजदीकी स्वास्थ्य सेवा प्रदाताओं से जुड़ें।',
      startChat: 'स्वास्थ्य परामर्श शुरू करें',
      emergencyCall: 'आपातकालीन सेवाएं',
      privacy: 'आपका स्वास्थ्य डेटा निजी और एन्क्रिप्टेड रहता है',
      tutorial: 'अपने लक्षणों को सामान्य भाषा में बताएं - हम समझते हैं'
    }
  };

  const currentLang = translations[selectedLanguage] || translations.en;

  const handleStartChat = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      console.log('Starting chat consultation...');
      navigate('/dashboard');
      
    }, 2000);
  };

  const emergencyNumbers = {
    en: { number: '108', label: 'Emergency Ambulance' },
    hi: { number: '108', label: 'आपातकालीन एम्बुलेंस' }
  };

  return (
    <div className={styles.landingContainer}>
      <div className={styles.animatedBg}>
        <div className={styles.floatingShapes}>
          <div className={`${styles.shape} ${styles.shape1}`}></div>
          <div className={`${styles.shape} ${styles.shape2}`}></div>
          <div className={`${styles.shape} ${styles.shape3}`}></div>
          <div className={`${styles.shape} ${styles.shape4}`}></div>
        </div>
      </div>
{/* 
       <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logo}>
            <div className={styles.logoIcon}>
              <div className={styles.heartbeat}>❤️</div>
            </div>
            <div className={styles.logoText}>
              <span className={styles.brandName}>{currentLang.title}</span>
              <span className={styles.brandTagline}>{currentLang.tagline}</span>
            </div>
          </div>
          
          <div className={styles.headerActions}>
            <div className={styles.languageSelector}>
              <select 
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className={styles.languageDropdown}
              >
                {Object.entries(languages).map(([code, lang]) => (
                  <option key={code} value={code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>
            
            <button 
              className={styles.emergencyBtn}
              onClick={() => window.open(`tel:${emergencyNumbers[selectedLanguage]?.number || '108'}`)}
            >
              🚨 Emergency
            </button>
          </div>
        </div>
      </header>
       */}
      {/* PWA Install Banner */}
      {showInstallPrompt && (
        <div className={`${styles.installBanner} ${styles.slideDown}`}>
          <div className={styles.installContent}>
            <div className={styles.installIcon}>📱</div>
            <span>Install SehatSathi for instant offline access</span>
            <div className={styles.installActions}>
              <button onClick={handleInstallClick} className={styles.installBtn}>
                Install App
              </button>
              <button 
                onClick={() => setShowInstallPrompt(false)}
                className={styles.dismissBtn}
              >
                Later
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className={styles.mainContent}>
        {/* Hero Section */}
        <section className={styles.heroSection} ref={heroRef}>
          <div className={styles.heroContent}>
            <div className={styles.heroBadge}>
              <span className={styles.badgeIcon}>🏆</span>
            </div>

            <h1 
              className={styles.heroTitle}
              style={{
                transform: `translate(${mousePosition.x * 0.1}px, ${mousePosition.y * 0.1}px)`
              }}
            >
              {currentLang.subtitle}
            </h1>

            <p className={styles.heroDescription}>
              {currentLang.description}
            </p>

            {/* Rotating Tutorial Tips */}
            <div className={styles.tutorialCarousel}>
              <div className={styles.tutorialTip}>
                <span className={styles.tipIcon}>💡</span>
                <span className={styles.tipText}>
                  {tutorialTips[selectedLanguage]?.[currentTip] || tutorialTips.en[currentTip]}
                </span>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className={styles.ctaSection}>
              <button 
                className={`${styles.primaryCta} ${isLoading ? styles.loading : ''}`}
                onClick={handleStartChat}
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className={styles.loadingSpinner}></div>
                ) : (
                  <>
                    <span className={styles.ctaIcon}>🩺</span>
                    <span>{currentLang.startChat}</span>
                    <span className={styles.ctaArrow}>→</span>
                  </>
                )}
              </button>

              <button 
                className={styles.secondaryCta}
                onClick={() => setShowTutorial(true)}
              >
                <span className={styles.ctaIcon}>📖</span>
                {currentLang.howItWorks}
              </button>
            </div>

          </div>

          <div className={styles.heroVisual}>
            <div className={styles.phoneMockup}>
              <div className={styles.phoneScreen}>
                <div className={styles.chatPreview}>
                  <div className={`${styles.chatMessage} ${styles.user}`}>
                    <span>I have fever and headache</span>
                  </div>
                  <div className={`${styles.chatMessage} ${styles.bot}`}>
                    <span>Let me analyze your symptoms...</span>
                  </div>
                  <div className={styles.typingIndicator}>
                    <div className={styles.dot}></div>
                    <div className={styles.dot}></div>
                    <div className={styles.dot}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.statsSection}>
          <div className={styles.statsGrid}>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>50K+</div>
              <div className={styles.statLabel}>Consultations</div>
            </div>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>15K+</div>
              <div className={styles.statLabel}>Active Users</div>
            </div>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>94%</div>
              <div className={styles.statLabel}>Accuracy Rate</div>
            </div>
            <div className={styles.statItem}>
              <div className={styles.statNumber}>5+</div>
              <div className={styles.statLabel}>Languages</div>
            </div>
          </div>
        </section>

        <section className={styles.howItWorks}>
          <h2 className={styles.sectionTitle}>How SehatSathi Works</h2>
          <div className={styles.stepsContainer}>
            {currentLang.steps?.map((step, index) => (
              <div key={index} className={styles.stepItem}>
                <div className={styles.stepNumber}>{index + 1}</div>
                <div className={styles.stepContent}>
                  <p>{step}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className={styles.featuresSection}>
          <h2 className={styles.sectionTitle}>Why Choose SehatSathi?</h2>
          <div className={styles.featuresGrid}>
            <div className={`${styles.featureCard} ${styles.instant}`}>
              <div className={styles.featureIcon}>⚡</div>
              <h3>Instant AI Analysis</h3>
              <p>Get immediate symptom assessment powered by advanced medical AI algorithms</p>
            </div>
            
            <div className={`${styles.featureCard} ${styles.available}`}>
              <div className={styles.featureIcon}>🕐</div>
              <h3>24/7 Availability</h3>
              <p>Healthcare guidance available round the clock, even in remote areas</p>
            </div>
            
            <div className={`${styles.featureCard} ${styles.secure}`}>
              <div className={styles.featureIcon}>🔒</div>
              <h3>Bank-Level Security</h3>
              <p>Your health data is encrypted and never stored or shared</p>
            </div>
            
            <div className={`${styles.featureCard} ${styles.offline}`}>
              <div className={styles.featureIcon}>📱</div>
              <h3>Works Offline</h3>
              <p>Basic features available even without internet connection</p>
            </div>
            
            <div className={`${styles.featureCard} ${styles.multilingual}`}>
              <div className={styles.featureIcon}>🌐</div>
              <h3>Multi-Language</h3>
              <p>Supports local languages for better communication</p>
            </div>
            
            <div className={`${styles.featureCard} ${styles.referral}`}>
              <div className={styles.featureIcon}>🗺️</div>
              <h3>Smart Referrals</h3>
              <p>Connects you with nearby healthcare providers when needed</p>
            </div>
          </div>
        </section>

        {/* Trust Indicators
        <section className={styles.trustSection}>
          <div className={styles.trustContent}>
            <h3>Trusted Healthcare Partner</h3>
            <div className={styles.trustBadges}>
              <div className={styles.trustBadge}>
                <span className={styles.badgeIcon}>🏥</span>
                <span>Medical Board Approved</span>
              </div>
              <div className={styles.trustBadge}>
                <span className={styles.badgeIcon}>🔐</span>
                <span>HIPAA Compliant</span>
              </div>
              <div className={styles.trustBadge}>
                <span className={styles.badgeIcon}>⭐</span>
                <span>4.8/5 User Rating</span>
              </div>
            </div>
          </div>
        </section> */}
      </main>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <div className={styles.footerMain}>
            <div className={styles.footerBrand}>
              <div className={styles.footerLogo}>
                <span className={styles.logoIcon}>❤️</span>
                <span className={styles.brandName}>{currentLang.title}</span>
              </div>
              <p>Making healthcare accessible to every rural community</p>
            </div>
            
            <div className={styles.footerLinks}>
              <div className={styles.linkGroup}>
                <h4>Quick Links</h4>
                <a href="#about">About Us</a>
                <a href="#privacy">Privacy Policy</a>
                <a href="#terms">Terms of Service</a>
              </div>
              <div className={styles.linkGroup}>
                <h4>Support</h4>
                <a href="#help">Help Center</a>
                <a href="#contact">Contact Us</a>
                <a href="#faq">FAQ</a>
              </div>
            </div>
          </div>
          
          <div className={styles.footerBottom}>
            <p className={styles.privacyNote}>
              🔐 {currentLang.privacy}
            </p>
            <div className={styles.emergencyInfo}>
              <span className={styles.emergencyText}>🚨 Medical Emergency?</span>
              <button 
                className={styles.emergencyCall}
                onClick={() => window.open(`tel:${emergencyNumbers[selectedLanguage]?.number || '108'}`)}
              >
                Call {emergencyNumbers[selectedLanguage]?.number || '108'}
              </button>
            </div>
          </div>
        </div>
      </footer>

      {/* Tutorial Modal */}
      {showTutorial && (
        <div className={styles.tutorialModal}>
          <div className={styles.modalContent}>
            <button 
              className={styles.modalClose}
              onClick={() => setShowTutorial(false)}
            >
              ✕
            </button>
            <h3>How to Use SehatSathi</h3>
            <div className={styles.tutorialSteps}>
              {/* Tutorial content would go here */}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPage;

# database/seed_laws.py
# Run once: python -m database.seed_laws
from database.crud import bulk_insert_laws
import logging

logger = logging.getLogger(__name__)

IT_ACT_SECTIONS = [
    ("IT Act 2000", "Section 43",  "Penalty for damage to computer",
     "If any person without permission accesses, downloads, introduces virus, disrupts, denies access, or assists others to do so — liable to pay compensation.",
     "Compensation up to Rs. 1 crore", "unauthorized access,hacking,virus,damage,computer"),

    ("IT Act 2000", "Section 66",  "Computer related offences",
     "If any person dishonestly or fraudulently commits any act referred to in Section 43, imprisonment or fine.",
     "Up to 3 years imprisonment or fine up to Rs. 5 lakh or both",
     "hacking,fraud,dishonest,computer offence"),

    ("IT Act 2000", "Section 66A", "Punishment for sending offensive messages",
     "Sending grossly offensive or false information through communication service. (Note: Struck down by SC in 2015 in Shreya Singhal case)",
     "Struck down — not applicable", "offensive message,online harassment"),

    ("IT Act 2000", "Section 66B", "Punishment for dishonestly receiving stolen computer resource",
     "Receiving or retaining any stolen computer resource or communication device knowingly.",
     "Up to 3 years imprisonment or fine up to Rs. 1 lakh or both",
     "stolen device,receiving stolen,computer resource"),

    ("IT Act 2000", "Section 66C", "Punishment for identity theft",
     "Fraudulently or dishonestly making use of the electronic signature, password or any other unique identification feature of any other person.",
     "Up to 3 years imprisonment and fine up to Rs. 1 lakh",
     "identity theft,password theft,electronic signature,impersonation"),

    ("IT Act 2000", "Section 66D", "Punishment for cheating by personation using computer",
     "Cheating by personating using a computer resource or a communication device.",
     "Up to 3 years imprisonment and fine up to Rs. 1 lakh",
     "personation,impersonation,cheating,phishing"),

    ("IT Act 2000", "Section 66E", "Punishment for violation of privacy",
     "Intentionally capturing, publishing or transmitting the image of a private area of a person without consent.",
     "Up to 3 years imprisonment or fine up to Rs. 2 lakh or both",
     "privacy violation,image,voyeurism,intimate image"),

    ("IT Act 2000", "Section 66F", "Punishment for cyber terrorism",
     "Denying access to authorized personnel, accessing a protected system, introducing contaminant to cause death or damage or threaten unity of India.",
     "Imprisonment which may extend to life imprisonment",
     "cyber terrorism,critical infrastructure,national security"),

    ("IT Act 2000", "Section 67",  "Punishment for publishing obscene material",
     "Publishing or transmitting obscene material in electronic form.",
     "First conviction: up to 3 years and fine up to Rs. 5 lakh. Subsequent: up to 5 years and fine up to Rs. 10 lakh",
     "obscene,pornography,online content"),

    ("IT Act 2000", "Section 67A", "Punishment for publishing sexually explicit material",
     "Publishing or transmitting sexually explicit material in electronic form.",
     "First conviction: up to 5 years and fine up to Rs. 10 lakh. Subsequent: up to 7 years and fine up to Rs. 10 lakh",
     "sexual content,explicit material,online"),

    ("IT Act 2000", "Section 67B", "Punishment for child pornography",
     "Publishing or transmitting material depicting children in sexually explicit acts.",
     "First conviction: up to 5 years and fine up to Rs. 10 lakh. Subsequent: up to 7 years and fine up to Rs. 10 lakh",
     "child pornography,CSAM,minor,child exploitation"),

    ("IT Act 2000", "Section 69",  "Power to issue directions for interception/monitoring",
     "Government can issue directions for interception, monitoring or decryption of information through any computer resource in interest of national security.",
     "Non-compliance: up to 7 years imprisonment",
     "interception,surveillance,monitoring,decryption,national security"),

    ("IT Act 2000", "Section 70",  "Protected systems",
     "Government may declare any computer resource as protected. Unauthorized access to protected system is an offence.",
     "Up to 10 years imprisonment and fine",
     "protected system,critical infrastructure,unauthorized access"),

    ("IT Act 2000", "Section 72",  "Breach of confidentiality and privacy",
     "Any person having secured access to any electronic record, book, register disclosing such without consent of the person concerned.",
     "Up to 2 years imprisonment or fine up to Rs. 1 lakh or both",
     "confidentiality,privacy breach,data leak,disclosure"),

    ("IT Act 2000", "Section 72A", "Punishment for disclosure of information in breach of contract",
     "Disclosure of personal information in breach of a lawful contract, causing wrongful loss or gain.",
     "Up to 3 years imprisonment or fine up to Rs. 5 lakh or both",
     "data breach,personal information,breach of contract"),

    ("IT Act 2000", "Section 74",  "Publication for fraudulent purpose",
     "Whoever creates, publishes or otherwise makes available a Digital Signature Certificate for fraudulent purpose.",
     "Up to 2 years imprisonment or fine up to Rs. 1 lakh or both",
     "digital signature,fraud,certificate"),

    # IPC Sections commonly used in cybercrime
    ("IPC", "Section 420", "Cheating and dishonestly inducing delivery of property",
     "Cheating and thereby dishonestly inducing the person deceived to deliver any property — commonly applied in online fraud cases.",
     "Up to 7 years imprisonment and fine",
     "fraud,online fraud,cheating,financial fraud,UPI fraud"),

    ("IPC", "Section 465", "Punishment for forgery",
     "Making any false document or false electronic record with intent to cause damage — applicable to document forgery in cybercrime.",
     "Up to 2 years imprisonment or fine or both",
     "forgery,fake document,electronic record"),

    ("IPC", "Section 468", "Forgery for purpose of cheating",
     "Committing forgery intending that the document or record forged shall be used for purpose of cheating.",
     "Up to 7 years imprisonment and fine",
     "forgery,cheating,fraud"),

    ("IPC", "Section 500", "Punishment for defamation",
     "Whoever defames another person — applicable to online defamation and social media harassment cases.",
     "Up to 2 years imprisonment or fine or both",
     "defamation,online defamation,reputation,social media"),
]


def seed():
    logger.info("Seeding law references into MySQL...")
    count = bulk_insert_laws(IT_ACT_SECTIONS)
    print(f"✅ Seeded {len(IT_ACT_SECTIONS)} law references into database")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    seed()
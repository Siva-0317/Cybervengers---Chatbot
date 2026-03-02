# knowledge_base/collectors/custom_qa_builder.py
"""
Hand-crafted Q&A pairs covering:
- Indian cyber law (IT Act + IPC)
- Investigation procedures
- Digital forensics
- Common attack types
- Evidence handling
These are the most targeted records for the investigation use case.
"""

CUSTOM_QA_PAIRS = [
    # ── Indian Cyber Law ─────────────────────────────────────
    {
        "q": "What is Section 66C of the IT Act 2000?",
        "a": "Section 66C deals with identity theft. It punishes anyone who fraudulently or dishonestly uses the electronic signature, password, or any other unique identification feature of another person. The punishment is imprisonment up to 3 years and a fine up to Rs. 1 lakh."
    },
    {
        "q": "What constitutes cybercrime under Indian law?",
        "a": "Under the IT Act 2000 and its 2008 amendment, cybercrimes include: unauthorized access to computer systems (Section 66), identity theft (Section 66C), cheating by personation online (Section 66D), cyber terrorism (Section 66F), publishing obscene material online (Section 67), hacking (Section 43/66), and data theft. IPC sections 420 (fraud) and 465 (forgery) are also commonly applied."
    },
    {
        "q": "What is the punishment for hacking under Indian law?",
        "a": "Under Section 66 of the IT Act 2000, hacking (unauthorized access to a computer system with dishonest intent) is punishable with imprisonment up to 3 years, or a fine up to Rs. 5 lakh, or both. Civil liability under Section 43 can also result in compensation up to Rs. 1 crore."
    },
    {
        "q": "What is cyber terrorism under the IT Act?",
        "a": "Section 66F of the IT Act 2000 defines cyber terrorism as: accessing a protected computer system without authorization, introducing malware to cause damage, or denying access to authorized users with intent to threaten national security, sovereignty, or cause death or injury. The punishment is life imprisonment."
    },
    {
        "q": "What is CERT-In and what is its role?",
        "a": "CERT-In (Indian Computer Emergency Response Team) is the national nodal agency under the Ministry of Electronics and IT for responding to cybersecurity incidents. It issues security guidelines, vulnerability notes, advisories, and coordinates cyber incident response. Organizations are mandated to report cybersecurity incidents to CERT-In within 6 hours under the 2022 directions."
    },
    {
        "q": "What are the mandatory reporting requirements for cybersecurity incidents in India?",
        "a": "Under the CERT-In Directions 2022, organizations including service providers, intermediaries, data centers, and government organizations must report cybersecurity incidents to CERT-In within 6 hours of noticing them. Reportable incidents include data breaches, ransomware attacks, unauthorized access, DDoS attacks, and website defacement."
    },

    # ── Digital Forensics & Investigation ────────────────────
    {
        "q": "What is the chain of custody in digital forensics?",
        "a": "Chain of custody is the documented process tracking how digital evidence is collected, handled, transferred, analyzed, and stored. It ensures evidence integrity and admissibility in court. Every person who handles the evidence must be documented with timestamps. Any break in the chain can make evidence inadmissible."
    },
    {
        "q": "What are the steps in a digital forensic investigation?",
        "a": "1. Identification: Recognize potential evidence sources (devices, logs, networks). 2. Preservation: Prevent evidence alteration — create forensic images. 3. Collection: Acquire data using write blockers to avoid modification. 4. Examination: Extract relevant data from acquired images. 5. Analysis: Correlate and interpret findings. 6. Documentation: Record all actions with timestamps. 7. Presentation: Prepare findings for legal proceedings."
    },
    {
        "q": "What is a forensic image and why is it used?",
        "a": "A forensic image is a bit-for-bit exact copy of a storage device including all sectors, deleted files, and unallocated space. It is used to preserve original evidence while allowing investigators to work on the copy. Tools like dd, FTK Imager, and Autopsy are used. Hash values (MD5/SHA-256) verify image integrity."
    },
    {
        "q": "What tools are used in digital forensic investigations?",
        "a": "Common forensic tools include: Autopsy (open-source disk forensics), Volatility (memory forensics), Wireshark (network packet analysis), FTK Imager (disk imaging), Cellebrite (mobile forensics), EnCase (enterprise forensics), Sleuth Kit (file system analysis), and NetworkMiner (network forensic analysis)."
    },
    {
        "q": "What is volatile data and why must it be captured first?",
        "a": "Volatile data is information stored in RAM, CPU registers, and cache that is lost when the system is powered off. It includes running processes, network connections, logged-in users, encryption keys, and clipboard contents. In live forensics, volatile data must be captured before shutdown because it contains critical evidence not stored on disk."
    },
    {
        "q": "How do you investigate a phishing attack?",
        "a": "Steps: 1. Preserve the phishing email with full headers. 2. Analyze email headers to trace originating IP and mail servers. 3. Examine links — extract URLs without clicking (use URLScan.io, VirusTotal offline equivalents). 4. Identify spoofed domains or lookalike domains. 5. Check sender's email against known threat intel. 6. Identify victims who clicked links. 7. Analyze web server logs for callback attempts. 8. Apply IT Act Section 66D (cheating by personation)."
    },
    {
        "q": "How do you investigate a ransomware attack?",
        "a": "Steps: 1. Isolate affected systems immediately. 2. Preserve memory dumps before shutdown. 3. Identify ransomware family from ransom note and file extensions. 4. Check No More Ransom project for decryptors. 5. Analyze network logs for lateral movement and C2 communication. 6. Identify patient zero (initial infection vector). 7. Recover from clean backups. 8. Document under IT Act Section 66 (computer related offences) and Section 66F if critical infrastructure is targeted."
    },
    {
        "q": "What is log analysis in cyber investigation?",
        "a": "Log analysis examines records generated by systems, applications, and networks to reconstruct events. Key log types: Windows Event Logs (authentication, process execution), Web server access logs (HTTP requests), Firewall logs (connection attempts), DNS logs (domain lookups), and SIEM aggregated logs. Investigators look for failed logins, privilege escalation, unusual outbound connections, and data exfiltration indicators."
    },

    # ── Attack Types ─────────────────────────────────────────
    {
        "q": "What is SQL injection and how is it investigated?",
        "a": "SQL injection is an attack where malicious SQL code is inserted into input fields to manipulate database queries. Forensic investigation: examine web server access logs for UNION SELECT, OR 1=1, and comment sequences. Check database query logs for unauthorized data access. Identify exfiltrated data. Apply IT Act Section 66 and Section 43 for unauthorized access."
    },
    {
        "q": "What is a Man-in-the-Middle (MITM) attack?",
        "a": "A MITM attack occurs when an attacker secretly intercepts and potentially alters communications between two parties. Common techniques include ARP poisoning, DNS spoofing, SSL stripping, and rogue Wi-Fi access points. Detection: check ARP tables for duplicate MACs, SSL certificate anomalies, unexpected DNS responses. Applicable under IT Act Section 66 and Section 72 (breach of privacy)."
    },
    {
        "q": "What is a DDoS attack and how is it identified in logs?",
        "a": "A Distributed Denial of Service (DDoS) attack floods a target with traffic from multiple sources to make it unavailable. In logs, identify: massive spike in connection requests from multiple IPs, repeated requests to same endpoint, SYN flood patterns (half-open connections), UDP flood, or amplification attack signatures. IP geolocation analysis helps identify botnet sources."
    },
    {
        "q": "What is social engineering in cybercrime?",
        "a": "Social engineering manipulates people psychologically to divulge confidential information or perform actions. Types include phishing (email), vishing (voice calls), smishing (SMS), pretexting (fabricated scenarios), and baiting. Investigation involves analyzing communication records, identifying impersonated entities, and tracing financial transactions. Applicable under IPC Section 420 (cheating) and IT Act Section 66D."
    },
    {
        "q": "What are Indicators of Compromise (IOCs)?",
        "a": "IOCs are artifacts that indicate a system has been compromised. They include: malicious IP addresses, suspicious domain names, file hashes of known malware, unusual registry keys, abnormal network traffic patterns, unauthorized user accounts, and unexpected scheduled tasks. IOCs are used in threat hunting and incident response to identify scope of compromise."
    },
    {
        "q": "What is the MITRE ATT&CK framework?",
        "a": "MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations. It is organized into: Tactics (the why — e.g., Initial Access, Persistence, Exfiltration), Techniques (the how — e.g., Phishing, Registry Run Keys), and Sub-techniques (specific implementations). It is used for threat modeling, detection development, and incident response."
    },

    # ── Network Forensics ────────────────────────────────────
    {
        "q": "What is network forensics?",
        "a": "Network forensics is the capture, recording, and analysis of network traffic and events to discover the source of security attacks or investigate other network-based incidents. Tools: Wireshark, NetworkMiner, Zeek (Bro). Key artifacts: PCAP files, NetFlow records, DNS query logs, firewall logs, proxy logs. Investigators reconstruct sessions, identify data exfiltration, and trace attacker IP addresses."
    },
    {
        "q": "How do you trace the origin of a cyber attack?",
        "a": "Steps: 1. Collect all available logs (web server, firewall, IDS/IPS, DNS). 2. Identify the attacking IP address. 3. Check IP geolocation and WHOIS records. 4. Analyze network traffic patterns. 5. Look for VPN or TOR exit nodes (common for attackers to hide). 6. Cross-reference with threat intelligence feeds. 7. Coordinate with ISP for subscriber information using legal process. 8. Document under applicable IT Act sections."
    },

    # ── Mobile Forensics ─────────────────────────────────────
    {
        "q": "What is mobile device forensics?",
        "a": "Mobile forensics involves the recovery and analysis of digital evidence from mobile devices including smartphones, tablets, and GPS devices. Techniques: logical acquisition (app data, contacts, messages), physical acquisition (full flash memory dump), chip-off extraction (for damaged devices). Tools: Cellebrite UFED, Oxygen Forensics, MOBILedit. Key evidence: call records, SMS/WhatsApp messages, GPS location history, app usage logs."
    },

    # ── Malware Analysis ─────────────────────────────────────
    {
        "q": "What are the types of malware and how are they investigated?",
        "a": "Malware types: Virus (attaches to legitimate files), Worm (self-replicating across networks), Trojan (disguised as legitimate software), Ransomware (encrypts files for ransom), Spyware (surveillance without consent), Rootkit (hides malware presence), Keylogger (records keystrokes), Botnet (remote-controlled infected machines). Investigation: static analysis (file hashes, strings, PE headers), dynamic analysis (sandbox execution), behavioral analysis (network connections, registry changes, file system modifications)."
    },
    {
        "q": "What is a rootkit and how is it detected?",
        "a": "A rootkit is malicious software designed to hide its presence and provide privileged access to a system. Types: kernel-mode rootkits (most dangerous, modify OS kernel), user-mode rootkits, bootkit (modifies MBR). Detection: compare kernel structures in memory with known good values, use offline scanning (boot from external media), check for DKOM (Direct Kernel Object Manipulation), use tools like GMER, RootkitRevealer, or Volatility."
    },

    # ── Evidence & Legal ─────────────────────────────────────
    {
        "q": "What makes digital evidence admissible in Indian courts?",
        "a": "Under Section 65B of the Indian Evidence Act, electronic evidence is admissible if: 1. It was produced by a computer in regular use. 2. The computer was operating properly. 3. The information was regularly fed into the computer. 4. A certificate from a responsible person is provided. The certificate must include: device description, time period, regular use, proper functioning, and information authenticity. Hash verification is critical for integrity."
    },
    {
        "q": "What is Section 65B of the Indian Evidence Act?",
        "a": "Section 65B governs the admissibility of electronic records (digital evidence) in Indian courts. It requires a certificate from a person in a responsible official position stating: the computer produced the electronic record, the computer was operating properly, the record was produced during regular use, and the information was supplied to the computer in the ordinary course of activities. Without this certificate, electronic evidence may not be admitted."
    },
    {
        "q": "How should a cyber investigator handle a seized device?",
        "a": "Best practices: 1. Photograph the device and its connections before touching. 2. If on, consider live acquisition for volatile data. 3. Place in Faraday bag to prevent remote wipe (for mobile devices). 4. Do NOT attempt to access the device without write blocker. 5. Document serial numbers, model, and visible condition. 6. Label and seal with tamper-evident tape. 7. Maintain chain of custody documentation throughout. 8. Store in secure, climate-controlled environment."
    },
]


def get_custom_qa_records() -> list[dict]:
    records = []
    for pair in CUSTOM_QA_PAIRS:
        text = f"Question: {pair['q']}\nAnswer: {pair['a']}"
        records.append({
            "text":     text,
            "source":   "Custom Investigation QA",
            "category": "qa",
            "metadata": {"type": "custom", "question": pair["q"]}
        })
    return records
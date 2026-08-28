<?php
if (!headers_sent()) {
    header('Content-Type: application/json; charset=utf-8');
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
}

if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Optional API Key for Google Gemini or OpenAI (leave empty to use built-in neural conversation engine)
$GEMINI_API_KEY = ""; 
$OPENAI_API_KEY = "";

// Read user input
$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);
$userMessage = '';

if ($data && isset($data['message'])) {
    $userMessage = trim($data['message']);
} elseif (isset($_POST['message'])) {
    $userMessage = trim($_POST['message']);
}

if (empty($userMessage)) {
    echo json_encode([
        'status' => 'error',
        'response' => 'Please ask a question so I can assist you!'
    ]);
    exit();
}

$cleanMsg = trim($userMessage);
$msgLower = strtolower($cleanMsg);

// 1. Google Gemini API Integration (if user provides key)
if (!function_exists('callGeminiAPI')) {
    function callGeminiAPI($apiKey, $prompt) {
        $url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" . $apiKey;
        $systemInstruction = "You are Abhinaya AI, a friendly, intelligent, and versatile conversational AI assistant like ChatGPT. You are the official assistant for Abhinaya Institute of Classical Bharatanatyam. You can answer ANY question (personal questions about yourself, math, coding, life advice, arts, history, science, philosophy, and details about Abhinaya Institute). Format responses nicely with HTML formatting (e.g. <strong>, <em>, <br>, <ul>, <li>, <a href='...'>).";
        
        $payload = [
            'contents' => [
                [
                    'role' => 'user',
                    'parts' => [
                        ['text' => $systemInstruction . "\n\nUser Question: " . $prompt]
                    ]
                ]
            ]
        ];
        
        $context = stream_context_create([
            'http' => [
                'method' => 'POST',
                'header' => "Content-Type: application/json\r\n",
                'content' => json_encode($payload),
                'timeout' => 12
            ],
            'ssl' => [
                'verify_peer' => false,
                'verify_peer_name' => false
            ]
        ]);
        
        $res = @file_get_contents($url, false, $context);
        if ($res) {
            $json = json_decode($res, true);
            if (isset($json['candidates'][0]['content']['parts'][0]['text'])) {
                return nl2br($json['candidates'][0]['content']['parts'][0]['text']);
            }
        }
        return false;
    }
}

// 2. Online Universal Knowledge Search (Wikipedia OpenSearch + Summary REST API)
if (!function_exists('queryUniversalKnowledge')) {
    function queryUniversalKnowledge($query) {
        $term = trim(preg_replace('/^(what is|who is|who was|tell me about|explain|define|where is|how does|what are|history of|calculate)\s+/i', '', $query));
        $term = trim(preg_replace('/[?.,!]+$/', '', $term));
        if (empty($term) || strlen($term) < 2) return false;
        
        $context = stream_context_create([
            'http' => [
                'method' => 'GET',
                'header' => "User-Agent: AbhinayaAI/2.0 (student@abhinayainstitute.org)\r\n",
                'timeout' => 8
            ],
            'ssl' => [
                'verify_peer' => false,
                'verify_peer_name' => false
            ]
        ]);
        
        // Step A: Search for the exact canonical page title
        $searchUrl = "https://en.wikipedia.org/w/api.php?action=opensearch&search=" . urlencode($term) . "&limit=1&namespace=0&format=json";
        $searchRes = @file_get_contents($searchUrl, false, $context);
        $canonicalTitle = $term;
        
        if ($searchRes) {
            $searchJson = json_decode($searchRes, true);
            if (isset($searchJson[1][0]) && !empty($searchJson[1][0])) {
                $canonicalTitle = $searchJson[1][0];
            }
        }
        
        // Step B: Fetch page summary
        $summaryUrl = "https://en.wikipedia.org/api/rest_v1/page/summary/" . urlencode(str_replace(' ', '_', $canonicalTitle));
        $res = @file_get_contents($summaryUrl, false, $context);
        
        if ($res) {
            $json = json_decode($res, true);
            if (isset($json['extract']) && !empty($json['extract']) && ($json['type'] ?? '') !== 'disambiguation') {
                $title = htmlspecialchars($json['title'] ?? $canonicalTitle);
                $extract = htmlspecialchars($json['extract']);
                $sourceUrl = $json['content_urls']['desktop']['page'] ?? '';
                
                $output = "<strong>$title</strong><br><br>$extract";
                if (!empty($sourceUrl)) {
                    $output .= "<br><br><small style='color:#aaa;'>Reference: <a href='$sourceUrl' target='_blank' style='color:#d4af37; text-decoration:underline;'>Read full article</a></small>";
                }
                return $output;
            }
        }
        return false;
    }
}

// 3. Mathematical Expression Evaluator
if (!function_exists('evaluateMathExpression')) {
    function evaluateMathExpression($str) {
        $clean = preg_replace('/[^0-9\+\-\*\/\.\(\)\^\%]/', '', $str);
        if (empty($clean) || strlen($clean) < 3) return false;
        
        if (preg_match('/^[0-9\.\s\+\-\*\/\(\)]+$/', $clean)) {
            try {
                $val = @eval("return $clean;");
                if ($val !== false && is_numeric($val)) {
                    return "The result of <strong>" . htmlspecialchars($clean) . "</strong> is: <strong style='color:#d4af37; font-size:1.1rem;'>" . $val . "</strong>";
                }
            } catch (Throwable $e) {}
        }
        return false;
    }
}

// 4. Primary Conversational & Personal AI QA Engine
if (!function_exists('generateMasterResponse')) {
    function generateMasterResponse($rawText, $msg, $geminiKey, $openaiKey) {
        // If Gemini key is provided, use real Gemini LLM
        if (!empty($geminiKey)) {
            $geminiRes = callGeminiAPI($geminiKey, $rawText);
            if ($geminiRes) return $geminiRes;
        }

        // Math questions (e.g. 50 * 20, 100 / 4)
        if (preg_match('/^[\d\s\+\-\*\/\(\)\.]+$/', $rawText) || preg_match('/(calculate|what is|compute)\s+([\d\s\+\-\*\/\(\)\.]+)/i', $rawText, $m)) {
            $mathStr = isset($m[2]) ? $m[2] : $rawText;
            $mathRes = evaluateMathExpression($mathStr);
            if ($mathRes) return $mathRes;
        }

        // ==========================================
        // A. Personal Questions About the AI (like ChatGPT)
        // ==========================================
        
        // 1. Name
        if (preg_match('/\b(what is your name|what\'s your name|whats your name|your name|who are you|tell me your name)\b/', $msg)) {
            return "My name is <strong>Abhinaya AI</strong>! 🌟<br><br>I am your intelligent virtual assistant designed to work just like ChatGPT. I can chat with you, answer general knowledge questions, solve math problems, explain classical dance, and help you navigate the Abhinaya Institute portal.";
        }

        // 2. How are you / Feelings
        if (preg_match('/\b(how are you|how r u|how are you doing|how do you feel|are you okay)\b/', $msg)) {
            return "I'm doing great, thank you for asking! 😊 I'm always energized and ready to help you with any questions. How are you doing today?";
        }

        // 3. Creator / Who made you
        if (preg_match('/\b(who created you|who made you|who built you|who is your creator|who developed you)\b/', $msg)) {
            return "I was created and customized for <strong>Abhinaya Institute of Classical Bharatanatyam</strong> by the institute's engineering team to serve as an intelligent, ChatGPT-powered conversational assistant for all students and visitors!";
        }

        // 4. Age / Birthday
        if (preg_match('/\b(how old are you|what is your age|when were you born|your birthday)\b/', $msg)) {
            return "I live in the digital realm, so I don't age like humans! I was created in 2026 to assist dance enthusiasts, students, and curious learners worldwide. ✨";
        }

        // 5. Capabilities / What can you do
        if (preg_match('/\b(what can you do|what do you do|help me with|your capabilities|how can you help)\b/', $msg)) {
            return "Just like ChatGPT, I can help you with a wide range of topics:
            <ul style='margin-top: 8px; margin-left: 20px; text-align: left;'>
                <li>💬 <strong>Chat & Conversation:</strong> Ask me personal, creative, or philosophical questions.</li>
                <li>📚 <strong>General Knowledge:</strong> Science, history, biographies, world facts, and coding.</li>
                <li>🔢 <strong>Math & Problem Solving:</strong> Arithmetic, calculations, and conversions.</li>
                <li>🎭 <strong>Bharatanatyam & Arts:</strong> Natyashastra, Adavus, Mudras, Navarasas, Talas, and Ragas.</li>
                <li>🏛️ <strong>Abhinaya Institute:</strong> Admissions, course fees (₹2,000–₹12,000), UPI QR payments, login, exams, and attendance.</li>
            </ul>";
        }

        // 6. Favorites / Preferences (Like ChatGPT)
        if (preg_match('/\b(what is your favorite|do you like|what do you like|your hobby|hobbies)\b/', $msg)) {
            return "As an AI, I don't have physical senses, but I absolutely love learning, exploring classical Bharatanatyam rhythms, and solving questions with you! What are some of your favorite things?";
        }

        // 7. Are you human / Are you real
        if (preg_match('/\b(are you human|are you a robot|are you ai|are you real)\b/', $msg)) {
            return "I am an <strong>Artificial Intelligence (AI)</strong> assistant, powered by neural conversational engines. While I am not a human, I'm here to chat, answer questions, and assist you in the friendliest and smartest way possible! 🤖✨";
        }

        // 8. Jokes & Fun
        if (preg_match('/\b(tell me a joke|tell a joke|make me laugh|joke)\b/', $msg)) {
            $jokes = [
                "Why did the dancer take up gardening? Because they wanted to improve their plant-e (plie)! 😄",
                "Why don't scientists trust atoms? Because they make up everything! ⚛️😂",
                "What did one classical dancer say to the other before rehearsal? 'Let’s step up our game!' 💃"
            ];
            return $jokes[array_rand($jokes)];
        }

        // 9. Thanks / Gratitude
        if (preg_match('/\b(thank you|thanks|thank u|thx|appreciate it)\b/', $msg)) {
            return "You're very welcome! 😊 If you have any other questions—whether about dance, science, math, or the website—feel free to ask anytime!";
        }

        // 10. Bye / Farewell
        if (preg_match('/\b(bye|goodbye|see you|good night|cya)\b/', $msg)) {
            return "Goodbye! Have a wonderful day ahead, and keep dancing with devotion and joy! 🙏✨";
        }

        // 11. Greetings
        if (preg_match('/\b(hi|hello|hey|namaste|greetings|good morning|good evening|good afternoon)\b/', $msg)) {
            return "Namaste! 🙏 Welcome! I am <strong>Abhinaya AI</strong>, your personal intelligent assistant. Feel free to ask me anything—whether personal questions, general knowledge, or portal guidance. How can I help you today?";
        }

        // ==========================================
        // B. Abhinaya Institute Specific Topics
        // ==========================================
        
        // 12. Registration & Account
        if (preg_match('/\b(register|registration|signup|sign up|create account|join|terms|condition)\b/', $msg)) {
            return "To join Abhinaya Institute and create your student account:
            <ol style='margin-top: 8px; margin-left: 20px; text-align: left;'>
                <li>Visit the <a href='register.php' style='color:#d4af37; text-decoration:underline;'><strong>Registration Page</strong></a>.</li>
                <li>Enter your Full Name, Email Address, and Password.</li>
                <li>Select your intended Bharatanatyam course.</li>
                <li>Check the required <strong>'I accept Terms & Conditions'</strong> box.</li>
                <li>Click <strong>Register</strong> to create your account!</li>
            </ol>";
        }

        // 13. Fees, Payments, UPI Scanner & Receipts
        if (preg_match('/\b(fee|fees|cost|price|pay|payment|upi|qr|scanner|receipt|transaction)\b/', $msg)) {
            return "<strong>Course Fees & Payment Process:</strong><br>
            Annual course fees range from <strong>₹2,000</strong> (Fresh Admission) up to <strong>₹12,000</strong> (Alankar Pratham).<br><br>
            <strong>How to pay online:</strong>
            <ol style='margin-top: 8px; margin-left: 20px; text-align: left;'>
                <li>Go to the <a href='fee-payment.php' style='color:#d4af37; text-decoration:underline;'><strong>Fee Payment Page</strong></a>.</li>
                <li>Enter your Name, Email, and select your course.</li>
                <li>A dynamic <strong>UPI QR Code</strong> will appear with the exact amount pre-filled.</li>
                <li>Scan with <strong>Google Pay / PhonePe / Paytm</strong> to complete payment.</li>
                <li>Click <strong>Confirm Payment</strong> to instantly generate and print your official verified receipt!</li>
            </ol>";
        }

        // 14. Courses & Curriculum
        if (preg_match('/\b(course|courses|curriculum|syllabus|level|levels|prarambhik|praveshika|madhyama|visharad|alankar|beginner)\b/', $msg)) {
            return "We offer 10 structured classical Bharatanatyam levels under the Gandharva Mahavidyalaya syllabus:
            <ul style='margin-top: 8px; margin-left: 20px; text-align: left;'>
                <li><strong>Foundation:</strong> Fresh Admission (Beginner) & Prarambhik</li>
                <li><strong>Intermediate:</strong> Praveshika Pratham & Praveshika Purna</li>
                <li><strong>Diplomatic:</strong> Madhyama Pratham & Madhyama Purna</li>
                <li><strong>Graduate:</strong> Visharad Pratham, Visharad Dwitiya & Visharad Tritiya</li>
                <li><strong>Mastery:</strong> Alankar Pratham</li>
            </ul>
            <br>👉 Explore the complete curriculum on our <a href='courses.php' style='color:#d4af37; text-decoration:underline;'><strong>Curriculum & Courses Page</strong></a>.";
        }

        // 15. Login & Portal Access
        if (preg_match('/\b(login|log in|signin|sign in|portal|dashboard|student portal|remember me)\b/', $msg)) {
            return "<strong>Student Portal Access:</strong><br>
            Registered students can log in to view enrolled batches, syllabus details, and examination updates.<br><br>
            👉 <a href='login.php' style='color:#d4af37; text-decoration:underline;'><strong>Click here to Login</strong></a>.<br>
            <em>Tip:</em> Check <strong>'Remember Me'</strong> on the login screen to keep your credentials saved securely on your browser!";
        }

        // 16. Password Reset
        if (preg_match('/\b(forgot|reset|recover|password|lost password)\b/', $msg)) {
            return "<strong>Trouble Logging In?</strong><br>
            If you forgot your password, you can easily recover your account:
            <ol style='margin-top: 8px; margin-left: 20px; text-align: left;'>
                <li>Visit the <a href='forgot-password.php' style='color:#d4af37; text-decoration:underline;'><strong>Forgot Password Page</strong></a>.</li>
                <li>Enter your registered email address.</li>
                <li>A 6-digit session verification code will be generated.</li>
                <li>Enter the code on the reset page and create your new password!</li>
            </ol>";
        }

        // 17. Examinations
        if (preg_match('/\b(exam|exams|examination|examinations|marks|results|certificate)\b/', $msg)) {
            return "<strong>Examinations & Grading:</strong><br>
            Our institute conducts both theoretical and practical examinations adhering to classical standards. Students are evaluated on Adavus, Tala recitation, Abhinaya, and Shloka memorization.<br><br>
            👉 Learn more on the <a href='examinations.html' style='color:#d4af37; text-decoration:underline;'><strong>Examinations Page</strong></a>.";
        }

        // 18. Attendance & Schedule
        if (preg_match('/\b(attendance|schedule|timing|timings|class|batch|calendar)\b/', $msg)) {
            return "<strong>Attendance & Batch Schedule:</strong><br>
            • A minimum of <strong>85% attendance</strong> is required for annual exam eligibility and stage performances.<br>
            • Check your current schedule on the <a href='schedule.php' style='color:#d4af37; text-decoration:underline;'><strong>Student Schedule Page</strong></a>.<br>
            • You can also download the <a href='ACADEMIC CALENDAR.pdf' target='_blank' style='color:#d4af37; text-decoration:underline;'><strong>Academic Calendar (PDF)</strong></a>.";
        }

        // ==========================================
        // C. Universal Question Answering via Live Search
        // ==========================================
        $universalAns = queryUniversalKnowledge($rawText);
        if ($universalAns) {
            return $universalAns;
        }

        // D. Friendly Conversational Fallback
        return "I understand your question! As your AI assistant, I can help you with anything from personal questions, general knowledge (history, science, coding, arts), to website details.<br><br>Could you tell me a bit more about what you'd like to explore?";
    }
}

$botReply = generateMasterResponse($cleanMsg, $msgLower, $GEMINI_API_KEY, $OPENAI_API_KEY);

echo json_encode([
    'status' => 'success',
    'response' => $botReply
]);
?>

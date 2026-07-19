import random

# A comprehensive dictionary mapping skills to interview questions
QUESTION_BANK = {
    # Python
    'Python': [
        {'question': 'What is the difference between deep and shallow copy in Python?', 'difficulty': 'Medium', 'hint': 'Mention copy() vs deepcopy() and how nested objects are handled.'},
        {'question': 'How does garbage collection work in Python?', 'difficulty': 'Hard', 'hint': 'Discuss reference counting and the generational garbage collector.'},
        {'question': 'What are decorators and how are they used?', 'difficulty': 'Medium', 'hint': 'Explain wrapper functions and the @ syntax.'},
        {'question': 'What is a generator in Python?', 'difficulty': 'Medium', 'hint': 'Mention the yield keyword and memory efficiency.'}
    ],
    # Java
    'Java': [
        {'question': 'Explain the difference between HashMap and ConcurrentHashMap.', 'difficulty': 'Medium', 'hint': 'Discuss thread safety and locking mechanisms.'},
        {'question': 'What is the JVM, JRE, and JDK?', 'difficulty': 'Easy', 'hint': 'Explain the execution environment vs development kit.'},
        {'question': 'How does garbage collection work in Java?', 'difficulty': 'Hard', 'hint': 'Mention minor/major GC, generational spaces (Eden, Survivor, Tenured).'},
        {'question': 'What are default methods in interfaces (Java 8+)?', 'difficulty': 'Easy', 'hint': 'Explain backward compatibility and multiple inheritance resolution.'}
    ],
    # JavaScript
    'JavaScript': [
        {'question': 'Explain event delegation in JavaScript.', 'difficulty': 'Medium', 'hint': 'Discuss event bubbling and attaching listeners to parent elements.'},
        {'question': 'What is the event loop?', 'difficulty': 'Hard', 'hint': 'Explain call stack, callback queue, and microtask queue.'},
        {'question': 'What is the difference between var, let, and const?', 'difficulty': 'Easy', 'hint': 'Discuss block scoping vs function scoping and hoisting.'},
        {'question': 'Explain closures in JavaScript.', 'difficulty': 'Medium', 'hint': 'Discuss accessing outer scope variables from inner functions.'}
    ],
    # React
    'React': [
        {'question': 'What is the Virtual DOM and how does React use it?', 'difficulty': 'Medium', 'hint': 'Explain reconciliation and diffing algorithm.'},
        {'question': 'Explain the useEffect hook and its dependency array.', 'difficulty': 'Easy', 'hint': 'Discuss side effects, component lifecycle, and preventing infinite loops.'},
        {'question': 'What is Context API and when would you use it over Redux?', 'difficulty': 'Medium', 'hint': 'Discuss prop drilling and global state management complexity.'},
        {'question': 'How can you optimize performance in a React application?', 'difficulty': 'Hard', 'hint': 'Mention React.memo, useMemo, useCallback, and code splitting.'}
    ],
    # Node.js
    'Node.js': [
        {'question': 'How does Node.js handle concurrency despite being single-threaded?', 'difficulty': 'Medium', 'hint': 'Explain the Event Loop, libuv, and asynchronous I/O.'},
        {'question': 'What are streams in Node.js?', 'difficulty': 'Medium', 'hint': 'Discuss readable, writable, duplex, and transform streams for handling large data.'},
        {'question': 'Explain the purpose of package.json and package-lock.json.', 'difficulty': 'Easy', 'hint': 'Discuss dependency versions, semantic versioning, and deterministic builds.'}
    ],
    # SQL
    'SQL': [
        {'question': 'Explain the different types of JOINs.', 'difficulty': 'Easy', 'hint': 'Describe INNER, LEFT, RIGHT, and FULL OUTER joins.'},
        {'question': 'What is the difference between WHERE and HAVING?', 'difficulty': 'Medium', 'hint': 'Discuss filtering before vs after GROUP BY aggregation.'},
        {'question': 'What are indexes and how do they improve performance?', 'difficulty': 'Medium', 'hint': 'Explain B-trees, clustered vs non-clustered indexes, and write overhead.'},
        {'question': 'Explain ACID properties in database transactions.', 'difficulty': 'Hard', 'hint': 'Atomicity, Consistency, Isolation, Durability.'}
    ],
    # MongoDB
    'MongoDB': [
        {'question': 'How does MongoDB differ from a relational database?', 'difficulty': 'Easy', 'hint': 'Discuss document-oriented vs table-oriented, schema flexibility, and scaling.'},
        {'question': 'Explain the concept of an aggregation pipeline.', 'difficulty': 'Medium', 'hint': 'Mention stages like $match, $group, $project, and $lookup.'}
    ],
    # Docker
    'Docker': [
        {'question': 'What is the difference between a Docker image and a container?', 'difficulty': 'Easy', 'hint': 'Image is the blueprint (read-only), container is the running instance.'},
        {'question': 'How do you persist data in Docker?', 'difficulty': 'Medium', 'hint': 'Discuss Volumes and Bind Mounts.'},
        {'question': 'Explain a multi-stage Docker build.', 'difficulty': 'Medium', 'hint': 'Discuss reducing final image size by separating build tools from runtime.'}
    ],
    # Kubernetes
    'Kubernetes': [
        {'question': 'What is a Pod in Kubernetes?', 'difficulty': 'Easy', 'hint': 'The smallest deployable computing unit, which can contain one or more containers.'},
        {'question': 'Explain the difference between a Deployment and a StatefulSet.', 'difficulty': 'Medium', 'hint': 'Discuss stateless vs stateful applications, ordering, and persistent identities.'}
    ],
    # AWS
    'AWS': [
        {'question': 'What is the difference between EC2 and Lambda?', 'difficulty': 'Easy', 'hint': 'IaaS (virtual machines) vs FaaS (serverless, event-driven).'},
        {'question': 'Explain the purpose of an IAM Role.', 'difficulty': 'Medium', 'hint': 'Delegating access securely without sharing long-term credentials.'}
    ],
    # Machine Learning / AI
    'Machine Learning': [
        {'question': 'What is the bias-variance tradeoff?', 'difficulty': 'Medium', 'hint': 'Discuss underfitting vs overfitting and model complexity.'},
        {'question': 'Explain cross-validation and why it is useful.', 'difficulty': 'Easy', 'hint': 'Discuss k-fold, preventing overfitting on training data, and evaluating generalization.'}
    ],
    'Deep Learning': [
        {'question': 'What is the vanishing gradient problem and how to mitigate it?', 'difficulty': 'Hard', 'hint': 'Discuss activation functions like ReLU, initialization (He/Xavier), and Batch Normalization.'},
        {'question': 'Explain the difference between CNNs and RNNs.', 'difficulty': 'Medium', 'hint': 'Spatial data (images) vs sequential data (time series, text).'}
    ],
    'NLP': [
        {'question': 'What is TF-IDF?', 'difficulty': 'Easy', 'hint': 'Term Frequency-Inverse Document Frequency, evaluating word importance.'},
        {'question': 'Explain the attention mechanism in Transformers.', 'difficulty': 'Hard', 'hint': 'Self-attention, query/key/value matrices, focusing on relevant parts of input.'}
    ]
}

# Fallback general questions
GENERAL_QUESTIONS = [
    {'question': 'Can you describe a challenging technical problem you solved recently?', 'skill': 'General', 'difficulty': 'Medium', 'hint': 'Use the STAR method (Situation, Task, Action, Result).'},
    {'question': 'How do you handle disagreements on technical approaches within a team?', 'skill': 'Soft Skills', 'difficulty': 'Medium', 'hint': 'Focus on communication, evidence-based discussion, and compromise.'},
    {'question': 'Explain a complex concept to me as if I were a non-technical stakeholder.', 'skill': 'Communication', 'difficulty': 'Hard', 'hint': 'Use analogies, avoid jargon, and focus on the "why" and business value.'},
    {'question': 'How do you stay updated with the latest technologies and trends?', 'skill': 'General', 'difficulty': 'Easy', 'hint': 'Mention blogs, courses, side projects, or community involvement.'}
]

def generate_interview_questions(skills: list, count: int = 5) -> list:
    """
    Generates rule-based interview questions based on the candidate's skills.
    
    Args:
        skills (list): List of skills extracted from the resume/JD.
        count (int): Number of questions to generate.
        
    Returns:
        list: A list of question dictionaries.
    """
    selected_questions = []
    
    # Try to find questions for the provided skills
    for skill in skills:
        skill_name = None
        for key in QUESTION_BANK.keys():
            if key.lower() == skill.lower():
                skill_name = key
                break
                
        if skill_name:
            questions = QUESTION_BANK[skill_name]
            available = [q for q in questions if q not in selected_questions]
            if available:
                q = random.choice(available)
                q_copy = q.copy()
                q_copy['skill'] = skill_name
                selected_questions.append(q_copy)
                
        if len(selected_questions) >= count:
            break
            
    # If we still need more questions, add some general/behavioral ones
    if len(selected_questions) < count:
        needed = count - len(selected_questions)
        available_general = [q for q in GENERAL_QUESTIONS if q not in selected_questions]
        
        to_add = random.sample(available_general, min(needed, len(available_general)))
        selected_questions.extend(to_add)
        
    # Shuffle for variety
    random.shuffle(selected_questions)
    
    return selected_questions[:count]

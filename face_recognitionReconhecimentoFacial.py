from flask import Flask, request, render_template
import cv2
import face_recognition

app = Flask(_name_)

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'GET':
        # Exibe um formulário HTML para o usuário movimentar o rosto para os lados
        return render_template('form.html')
    else:
        # Obtenha as imagens enviadas no formulário
        left_image = request.files['left_image']
        right_image = request.files['right_image']
        front_image = request.files['front_image']
        
        # Converta as imagens para arrays numpy
        left_image = cv2.cvtColor(cv2.imdecode(np.fromstring(left_image.read(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        right_image = cv2.cvtColor(cv2.imdecode(np.fromstring(right_image.read(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        front_image = cv2.cvtColor(cv2.imdecode(np.fromstring(front_image.read(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        
        # Use o face_recognition para obter informações sobre o rosto nas imagens
        left_face_landmarks = face_recognition.face_landmarks(left_image)
        right_face_landmarks = face_recognition.face_landmarks(right_image)
        front_face_landmarks = face_recognition.face_landmarks(front_image)
        
        # Verifique se foi encontrado pelo menos um rosto nas imagens
        if len(left_face_landmarks) == 0 or len(right_face_landmarks) == 0 or len(front_face_landmarks) == 0:
            return 'Nenhum rosto foi encontrado nas imagens'
        
        # Verifique se os olhos dos rostos estão abertos nas imagens
        left_eye_open = face_landmarks[0]['left_eye'][2][1] > face_landmarks[0]['left_eye'][0][1]
        right_eye_open = face_landmarks[0]['right_eye'][3][1] > face_landmarks[0]['right_eye'][1][1]
        
        if not left_eye_open or not right_eye_open:
            return 'Os olhos do rosto estão fechados'
        
        # Verifique se o rosto está usando óculos
        if 'nose_bridge' in face_landmarks[0]:
            return 'O rosto está usando óculos'
        
        # Caso contrário, retorne uma mensagem de sucesso
        return 'Rosto válido'

if _name_ == '_main_':
    app.run()

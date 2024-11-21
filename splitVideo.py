import cv2

def split_and_save_video(input_video, output_path):
    # Abrir o vídeo para leitura
    cap = cv2.VideoCapture(input_video)

    # Obter informações sobre o vídeo
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Criar objetos VideoWriter para salvar as duas metades
    out1 = cv2.VideoWriter(f"{output_path}/part1.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    out2 = cv2.VideoWriter(f"{output_path}/part2.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Dividir o vídeo ao meio
    middle_frame = total_frames // 2
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        current_frame += 1

        if current_frame <= middle_frame:
            out1.write(frame)  # gravar frames na primeira metade
        else:
            out2.write(frame)  # gravar frames na segunda metade

    # Liberar os recursos
    cap.release()
    out1.release()
    out2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    input_video = "My video - Data (2).mp4"  # caminho para o vídeo de entrada
    output_path = "output"  # diretório onde serão salvos os vídeos divididos

    split_and_save_video(input_video, output_path)

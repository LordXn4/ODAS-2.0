import onnxruntime as ort


def create_cpu_session_options(
    threads: int = 4,
) -> ort.SessionOptions:
    options = ort.SessionOptions()

    # Baixa latência sem criar dezenas de threads.
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1

    # Execução sequencial tende a ser mais previsível
    # para um assistente local com poucos recursos.
    options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

    # Evita logs desnecessários durante o uso normal.
    options.log_severity_level = 3

    return options

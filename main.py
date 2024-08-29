from utils import generate_json, compare_all_with_default, write_json_output, load_data, read_json_files_from_directory
from err import Errors


def main():
    RESPONSE = None

    try:
        # Gerar JSON de um único arquivo
        # generate_json()

        # Gerar JSON de múltiplos arquivos
        generate_json(multiple_files=True)

        # Gerar JSON de múltiplos arquivos de um mesmo banco
        # generate_json(multiple_db_files=True)

        default_data = load_data()
        data_files = read_json_files_from_directory()
        comparison_results = compare_all_with_default(default_data, *data_files)

        RESPONSE = write_json_output(data=comparison_results)
    except Errors as e:
        RESPONSE = e.get_response()
    except Exception as e:
        RESPONSE = Errors(code=1, message=f"{str(e)}").get_response()
    finally:
        print(RESPONSE)

if __name__ == '__main__':
    # RUNTIME TEST
    from time import time

    start_time = time()
    # ---------------

    main()

    # RUNTIME TEST
    end_time = time()

    print(f"\nTempo de execução: {round(end_time - start_time, 2)} segundos")
    # ---------------

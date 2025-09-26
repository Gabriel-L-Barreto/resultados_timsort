import time
import tracemalloc
import sys
import os
import threading
import xml.etree.ElementTree as ET

def insertion_sort(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    for i in range(left + 1, right + 1):
        key_item = arr[i]
        j = i - 1
        while j >= left and arr[j] > key_item:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr


def merge(left, right):
    merged = []
    i = 0
    j = 0
    len_left = len(left)
    len_right = len(right)
    while i < len_left and j < len_right:
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    if i < len_left:
        merged.extend(left[i:])
    if j < len_right:
        merged.extend(right[j:])
    return merged


def tim_sort(arr):
    min_run = 32
    n = len(arr)
    for i in range(0, n, min_run):
        insertion_sort(arr, i, min(i + min_run - 1, (n - 1)))
    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            midpoint = start + size
            end = min((start + size * 2 - 1), (n - 1))
            merged_array = merge(arr[start:midpoint], arr[midpoint:end + 1])
            arr[start:start + len(merged_array)] = merged_array
        size *= 2
    return arr


def main():
    if len(sys.argv) < 2:
        print("Uso: python timsort.py <arquivo_entrada.txt>")
        sys.exit(1)
    entrada = sys.argv[1]
    base = os.path.basename(entrada)
    nome, _sep, _ext = base.partition('.')
    saida_txt = f"saida_{nome}.txt"
    saida_xml = f"saida_{nome}.xml"

    with open(entrada, "r") as f:
        conteudo = f.read()
        a = list(map(int, conteudo.split()))

# 5 execuções
    runs = []
    sorted_list = None

    for run_idx in range(1, 6):
        a_copia = a[:]

        memoria_samples = []
        stop_event = threading.Event()

        def sample_memory():
            while not stop_event.is_set():
                current, _peak = tracemalloc.get_traced_memory()
                memoria_samples.append(current)
                time.sleep(0.01)

        tracemalloc.start()
        sampler_thread = threading.Thread(target=sample_memory, daemon=True)
        sampler_thread.start()

        inicio = time.perf_counter()
        resultado = tim_sort(a_copia)
        fim = time.perf_counter()

        stop_event.set()
        sampler_thread.join()

        memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if memoria_samples:
            memoria_media = sum(memoria_samples) / len(memoria_samples)
        else:
            memoria_media = float(memoria_atual)

#m etricas
        runs.append({
            "index": run_idx,
            "tempo": fim - inicio,
            "memoria_media": memoria_media / 1024.0,
            "memoria_pico": memoria_pico / 1024.0     
        })

        if sorted_list is None:
            sorted_list = resultado

    with open(saida_txt, "w") as f:
        f.write("Lista ordenada:\n")
        f.write(str(sorted_list) + "\n\n")

# XML
    root = ET.Element("timsort_runs", attrib={"input": base, "runs": str(len(runs))})
    for r in runs:
        run_el = ET.SubElement(root, "run", attrib={"index": str(r["index"])})
        tempo_el = ET.SubElement(run_el, "time_seconds")
        tempo_el.text = f"{r['tempo']:.6f}"
        mem_media_el = ET.SubElement(run_el, "memory_avg_kb")
        mem_media_el.text = f"{r['memoria_media']:.2f}"
        mem_peak_el = ET.SubElement(run_el, "memory_peak_kb")
        mem_peak_el.text = f"{r['memoria_pico']:.2f}"

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0) if hasattr(ET, 'indent') else None
    with open(saida_xml, "wb") as f_xml:
        tree.write(f_xml, encoding="utf-8", xml_declaration=True)

    print(f"\nOrdenação concluída! TXT salvo em '{saida_txt}' e XML salvo em '{saida_xml}'.")


if __name__ == "__main__":
    main()

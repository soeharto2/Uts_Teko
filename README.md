1. Mengapa `power()` dipanggil di dalam `term()`?

Karena precedence operator bekerja dari level tertinggi ke terendah.

Hierarki matematika:


()
^
* /
+ -


Artinya parser harus menyelesaikan operator pangkat dulu sebelum perkalian.

Kalau kamu memanggil `term()` di dalam `power()`, precedence jadi rusak. Parser bisa menganggap:

a ^ 2 * b

sebagai:

a ^ (2 * b)

padahal yang benar:

(a ^ 2) * b


Ini bukan sekadar “urutan function”. Ini representasi langsung dari grammar precedence.

Struktur parser yang benar:

expr   -> term
term   -> power
power  -> factor

Semakin ke bawah, semakin tinggi prioritas operatornya 

2. Apa yang terjadi jika variabel `z` tidak ada di `symbol_table`?

Parser akan masuk fase Analisis Semantik dan melempar error:


Semantic Error: Undefined variable 'z'

Contoh:

source_code = "a + z"

dengan:

symbol_table = {'a': 1}

maka:

Error: Semantic Error: Undefined variable 'z'


Ini penting karena lexer dan parser hanya memeriksa struktur sintaks.

Mereka tidak tahu apakah variabel benar-benar “valid”.

Analisis semantik bertugas memastikan:

* variabel ada
* tipe data valid
* operasi legal
* scope benar

Tanpa semantic analysis, compiler bisa menghasilkan kode untuk variabel yang tidak pernah dideklarasikan 

3. Mengapa `a ^ 2` harus muncul sebelum `+` di TAC?

Karena TAC mengikuti dependency evaluation.

Ekspresi:

a ^ 2 + b * c

tidak bisa langsung dijumlahkan sebelum operand selesai dihitung.

Compiler harus membangun nilai intermediate dulu:

t1 = a ^ 2
t2 = b * c
t3 = t1 + t2

Kalau compiler mencoba:

t1 = ? + ?

sebelum hasil operand tersedia, maka operand belum punya nilai.

Ini prinsip dasar code generation:

* operasi terdalam dulu
* hasil disimpan di temporary variable
* baru operasi level atas dieksekusi


from pathlib import Path

p = Path("Lab04/typst/CpadLabAssignment04ChaitanyaShinde231070066.typ")
text = p.read_text()

text = text.replace("($200 USD", r"(\$200 USD")
text = text.replace("$(0.5, 1.0)$", "(0.5, 1.0)")
text = text.replace('($"scale" propto 1/cos phi$)', "(scale proportional to 1/cos(phi))")
text = text.replace("$pm 85.051129^circ$", "±85.051129°")

p.write_text(text)
print("Updated math & dollar signs successfully.")

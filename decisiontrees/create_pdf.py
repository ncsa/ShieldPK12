#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Sun June 11 16:00:00 2017
@author: Jorj McKie
Copyright (c) 2017-2020 Jorj X. McKie
The license of this program is governed by the GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007 or later.
Demo program for the Python binding PyMuPDF of MuPDF.
Dependencies:
-------------
* PyMuPDF v1.17.4
* calendar (either use LocaleTextCalendar or just TextCalendar)
This program creates calendars for three years in a row (starting with
the one given as parameter) and stores the result in a PDF.
"""
import fitz


if __name__== "__main__":
    if not fitz.VersionBind.split(".") >= ["1", "17", "4"]:
        raise ValueError("Need PyMuPDF v.1.17.4 at least.")

    doc = fitz.open()  # new empty PDF
    # font = fitz.Font("cour")  # use the built-in font Courier
    font = fitz.Font("spacemo")  # use Space Mono - a nicer mono-spaced font

    page_rect = fitz.PaperRect("letter-p")  # letter portrait
    w = page_rect.width
    h = page_rect.height
    print_rect = page_rect + (36, 72, -36, -36)  # fill this rectangle
    fontsize = 16

    # widget = fitz.Widget()
    # widget.rect = page_rect
    # widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
    # widget.field_name = "Policy for specialists meeting with students"
    # widget.field_value = "Yes"
    # widget.text_font = "ZaDb"
    # widget.text_fontsize = 0
    # page = doc.newPage(width=w, height=h)
    # page.addWidget(widget)
    # doc.save("check.pdf")

    text_list = ["A playbook app to help K-12 schools and administrators make decisions related to COVID-19, "
            "access targeted resources and make plans for implementation.",
            "xxxxx",
            "bbbbb",
            "ccccc"]
    page = doc.newPage(width=w, height=h)
    tw = fitz.TextWriter(page_rect)
    for text in text_list:
        tw.fillTextbox(print_rect, text, font=font, fontsize=fontsize)

    tw.writeText(page)
    doc.save("test.pdf", garbage=4, deflate=True, pretty=True)

    doc.close()

from .forms import *
from django.shortcuts import redirect, render
from django.db import connection
import pandas as pd
import pandas.io.sql as sql
from io import StringIO
import datetime
import numpy as np
from django.http import HttpResponse
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
import reportlab.lib.styles
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak



# sys.setdefaultencoding('utf-8')

from reportlab.lib.units import mm


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200 * mm, 20 * mm,
                             "Page %d of %d" % (self._pageNumber, page_count))


def patient_create(request, uuid=0):
    if request.method == "GET":
        if uuid == 0:
            form = PatientForm()
        else:
            patient = Patient.objects.get(pk=uuid)

            form = PatientForm(instance=patient)
        return render(request, "app/insert.html", {'form': form})
    else:
        if uuid == 0:
            form = PatientForm(request.POST, request.FILES)
        else:
            patient = Patient.objects.get(pk=uuid)
            form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
        return redirect('list/')


def patient_list(request):
    data = {'Patients': Patient.objects.all()}
    return render(request, 'app/show.html', data)


def patient_delete(request, id):
    patient_object = Patient.objects.get(pk=id)
    patient_object.delete()
    return redirect('/')


def module_create(request, uuid=0):
    if request.method == "GET":
        if uuid == 0:
            form = ModuleForm()
        else:
            module = insurance.objects.get(pk=uuid)

            form = ModuleForm(instance=module)
        return render(request, "app/module_insert.html", {'form': form})
    else:
        if uuid == 0:
            form = ModuleForm(request.POST, request.FILES)
        else:
            module = insurance.objects.get(pk=uuid)
            form = ModuleForm(request.POST, request.FILES, instance=module)
        if form.is_valid():
            form.save()
        return redirect('/patient/module3/list/')


def module_list(request):
    data = {'Module3s': insurance.objects.all()}
    return render(request, 'app/module_list.html', data)


def module_delete(request, uuid):
    module3 = insurance.objects.get(uuid=uuid)
    module3.delete()
    return redirect('/patient/module3/list/')


def module2_create(request, uuid=0):
    if request.method == "GET":
        if uuid == 0:
            form = Module2Form()
        else:
            module2 = medical_conditions.objects.get(pk=uuid)

            form = Module2Form(instance=module2)
        return render(request, "app/module2_insert.html", {'form': form})
    else:
        if uuid == 0:
            form = Module2Form(request.POST, request.FILES)
        else:
            module2 = medical_conditions.objects.get(pk=uuid)
            form = Module2Form(request.POST, request.FILES, instance=module2)
        if form.is_valid():
            form.save()
        return redirect('/patient/module2/list/')


def module2_list(request):
    data = {'Module2s': medical_conditions.objects.all().order_by('ICD_code')}
    return render(request, 'app/module2_list.html', data)


def module2_delete(request, uuid):
    module2 = medical_conditions.objects.get(uuid=uuid)
    module2.delete()
    return redirect('/patient/module2/list/')


def mp_create(request, uuid=0):
    if request.method == "GET":
        if uuid == 0:
            form = MedicalProblemsForm()
        else:
            mp = MedicalProblems.objects.get(pk=uuid)

            form = MedicalProblemsForm(instance=mp)
        return render(request, "app/mp_insert.html", {'form': form})
    else:
        if uuid == 0:
            form = MedicalProblemsForm(request.POST, request.FILES)
        else:
            mp = MedicalProblems.objects.get(pk=uuid)
            form = MedicalProblemsForm(request.POST, request.FILES, instance=mp)
        if form.is_valid():
            form.save()
        return redirect('/patient/medical-problems/list/')


def mp_list(request):
    data = {'Mps': MedicalProblems.objects.all()}
    return render(request, 'app/mp_list.html', data)


def mp_delete(request, uuid):
    Mp = MedicalProblems.objects.get(uuid=uuid)
    Mp.delete()
    return redirect('/patient/medical-problems/list/')


def result(request):
    context = {'data': Patient.objects.all().order_by('last_name')}

    return render(request, "app/result.html", context)


# def download_excel(request):
#     sio = StringIO()
#     x = 0.25
#     y = 0.25
#     Sc = int((x + y) * 30)
#
#     con = connect(user="root", password="12345", host="localhost", database="demo")
#
#     q = '''select p.full_name as Patient_Name, group_concat(distinct concat(ins.insurance_name, '-' ,
#       ins.effective_date, '-', ins.claim) separator '/') as Insurance_Effective_Date_claim,
#       group_concat(distinct mp.name) as Medicalproblems from patient p left join patient_medical_conditions pmc
#       on p.uuid  = pmc.patient_id left join medical_conditions mc on pmc.medical_conditions_id = mc.uuid left join
#       medical_problems mp on mc.medicalprobs_id = mp.uuid left join patient_insurance pis on p.uuid = pis.patient_id
#       left join insurance ins on pis.insurance_id = ins.uuid group by p.uuid; '''
#
#     df = sql.read_sql(q, con)
#     df.replace(to_replace=[None, ''], value='-', inplace=True)
#     PandasWriter = pd.ExcelWriter(sio, engine='xlsxwriter')
#     sheet = str(datetime.datetime.now().time()).replace(':', '.') + '_sheet'
#     df.to_excel(PandasWriter, sheet_name=sheet, encoding='utf-8', index=False, startrow=Sc, startcol=0)
#     s = PandasWriter.sheets[sheet]
#     s.insert_image('A1', 'healthviewX_logo_final.jpg', {'x_scale': x, 'y_scale': y})
#     s.write('C13', "Patient Details")
#     PandasWriter.save()
#     sio.seek(0)
#     workbook = sio.getvalue()
#     filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':',
#                                                                                                        '.') + '.xlsx'
#     response = HttpResponse(workbook, content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename=%s' % filename
#     return response
#
#
# def download_pdf(request):
#
#     file = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
#     with connection.cursor() as cursor:
#         con = cursor(user="root", password="12345", host="localhost", database="demo")
#         con = cursor.execute('''select p.full_name as Patient_Name,p.mobile_number as Mobile, group_concat(distinct concat(ins.insurance_name, '-' ,
#               ins.effective_date, '-', ins.claim) separator '/') as Insurance_Effective_Date_claim, group_concat(distinct mp.name) as Medicalproblems from patient p
#               left join patient_medical_conditions pmc on p.uuid  = pmc.patient_id left join medical_conditions mc on
#               pmc.medical_conditions_id = mc.uuid left join medical_problems mp on mc.medicalprobs_id = mp.uuid left join
#               patient_insurance pis on p.uuid = pis.patient_id left join insurance ins on pis.insurance_id = ins.uuid group by
#               p.uuid; ''')
#     df = sql.read_sql(q, con)
#     df.replace(to_replace=[None, ''], value='-', inplace=True)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=%s' % file
#     elements = []
#     data = [df.columns.to_list()] + df.values.tolist()
#     for a in data[1:]:
#         for index, val in enumerate(a):
#             if index == 2:
#                 b = str(val)
#                 #a[index] = Paragraph(b)
#                 a[index] = b.replace('/', '\n')
#                 continue
#             a[index] = Paragraph(val)
#     style = TableStyle(
#         [
#             ("BOX", (0, 0), (-1, -1), 1, colors.black),
#             ("GRID", (0, 0), (-1, -1), 1, colors.black),
#             ("BACKGROUND", (0, 0), (7, 0), colors.gray),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
#             ("ALIGN", (0, 0), (-1, -1), "LEFT"),
#             ("BACKGROUND", (0, 1), (-1, -1), colors.white),
#             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#         ]
#     )
#     s = getSampleStyleSheet()
#     title_style = s['Heading1']
#     title_style.alignment = 1
#     title = Paragraph("Patient Details ", title_style)
#     elements.append(title)
#     table = Table(data, style=style)
#     doc = SimpleDocTemplate(response)
#     elements.append(table)
#     doc.build(elements)
#     return response
#
#
# def download_csv(request):
#     sio = StringIO()
#     con = connect(user="root", password="12345", host="localhost", database="demo")
#     q = '''select p.full_name as Patient_Name, group_concat(distinct concat(ins.insurance_name, '-' ,
#       ins.effective_date, '-', ins.claim) separator '/') as Insurance_Effective_Date_claim, group_concat(distinct mp.name) as Medicalproblems from patient p
#       left join patient_medical_conditions pmc on p.uuid  = pmc.patient_id left join medical_conditions mc on
#       pmc.medical_conditions_id = mc.uuid left join medical_problems mp on mc.medicalprobs_id = mp.uuid left join
#       patient_insurance pis on p.uuid = pis.patient_id left join insurance ins on pis.insurance_id = ins.uuid group by
#       p.uuid; '''
#     df = sql.read_sql(q, con)
#     df.replace(to_replace=[None, ''], value='-', inplace=True)
#     filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':',
#                                                                                                        '.') + '.csv'
#     df.to_csv(sio)
#     sio.seek(0)
#     workbook = sio.getvalue()
#     response = HttpResponse(workbook, content_type='application/csv')
#     response['Content-Disposition'] = 'attachment; filename=%s' % filename
#     return response

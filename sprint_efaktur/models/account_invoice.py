# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=W0622

import base64

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


def _csv_row(data, delimiter=",", quote='"'):
    return (
        quote
        + (quote + delimiter + quote).join(
            [str(x).replace(quote, "\\" + quote) for x in data]
        )
        + quote
        + "\n"
    )


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _prepare_header_1(self):
        header_1 = [
            "FK",
            "KD_JENIS_TRANSAKSI",
            "FG_PENGGANTI",
            "NOMOR_FAKTUR",
            "MASA_PAJAK",
            "TAHUN_PAJAK",
            "TANGGAL_FAKTUR",
            "NPWP",
            "NAMA",
            "ALAMAT_LENGKAP",
            "JUMLAH_DPP",
            "JUMLAH_PPN",
            "JUMLAH_PPNBM",
            "ID_KETERANGAN_TAMBAHAN",
            "FG_UANG_MUKA",
            "UANG_MUKA_DPP",
            "UANG_MUKA_PPN",
            "UANG_MUKA_PPNBM",
            "REFERENSI",
            "KODE_DOKUMEN_PENDUKUNG",
        ]
        return header_1

    @api.multi
    def _prepare_header_2(self):
        header_2 = [
            "LT",
            "NPWP",
            "NAMA",
            "JALAN",
            "BLOK",
            "NOMOR",
            "RT",
            "RW",
            "KECAMATAN",
            "KELURAHAN",
            "KABUPATEN",
            "PROPINSI",
            "KODE_POS",
            "NOMOR_TELEPON",
        ]
        return header_2

    @api.multi
    def _prepare_header_3(self):
        header_3 = [
            "OF",
            "KODE_OBJEK",
            "NAMA",
            "HARGA_SATUAN",
            "JUMLAH_BARANG",
            "HARGA_TOTAL",
            "DISKON",
            "DPP",
            "PPN",
            "TARIF_PPNBM",
            "PPNBM",
        ]
        return header_3

    @api.multi
    def _prepare_data_header(self):
        self.ensure_one()
        data = {
            "ID_KETERANGAN_TAMBAHAN": "",
            "FG_UANG_MUKA": 0,
            "UANG_MUKA_DPP": 0,
            "UANG_MUKA_PPN": 0,
            "UANG_MUKA_PPNBM": 0,
            "REFERENSI": "",
            "JUMLAH_PPNBM": 0,
            "JALAN": "",
            "NOMOR_TELEPON": "",
            "BLOK": "",
            "NOMOR": "",
            "RT": "",
            "RW": "",
            "KECAMATAN": "",
            "KELURAHAN": "",
            "KABUPATEN": "",
            "PROPINSI": "",
            "KODE_POS": "",
            "JUMLAH_BARANG": 0,
            "TARIF_PPNBM": 0,
            "PPNBM": 0,
            "KODE_DOKUMEN_PENDUKUNG": "",
        }
        return data

    @api.multi
    def _prepare_data_detail(self, list_code_acc_exceptions):
        self.ensure_one()
        data = {
            "KODE_OBJEK": "",
            "NAMA": self.name or "",
            "HARGA_SATUAN": 0,
            "JUMLAH_BARANG": 1,
            "HARGA_TOTAL": 0,
            "DPP": self._get_jumlah_dpp(list_code_acc_exceptions),
            "DISKON": 0,
            "PPN": self.amount_tax,
        }
        return data

    @api.multi
    def _prepare_attachment_data(self, datas):
        data = {
            "name": "sprint_efaktur.csv",
            "datas": datas,
            "datas_fname": "efaktur_%s.csv" % (fields.Datetime.now().replace(" ", "_")),
            "type": "binary",
        }
        return data

    @api.multi
    def _get_alamat(self):
        self.ensure_one()
        street = self.partner_id.commercial_partner_id.street or ""
        street2 = self.partner_id.commercial_partner_id.street2 or ""
        city = self.partner_id.commercial_partner_id.city or ""
        zip = self.partner_id.commercial_partner_id.zip or ""
        alamat = street + ". " + street2 + ". " + city + ". " + zip
        return alamat

    @api.multi
    def _get_jumlah_dpp(self, list_code_acc_exceptions):
        self.ensure_one()
        result = 0
        for line in self.invoice_line:
            if line.account_id.code in list_code_acc_exceptions:
                continue
            if line.price_subtotal > 0:
                result += line.price_subtotal
        return result

    @api.multi
    def _generate_efaktur_invoice(self, delimiter, list_code_acc_exceptions):
        header_1 = self._prepare_header_1()
        header_2 = self._prepare_header_2()
        header_3 = self._prepare_header_3()
        result = "{}{}{}".format(
            _csv_row(header_1, delimiter),
            _csv_row(header_2, delimiter),
            _csv_row(header_3, delimiter),
        )

        for document in self:
            if document.state != "draft":
                data = document._prepare_data_header()
                no_faktur = document.enofa_nomor_dokumen.replace(".", "")
                alamat_lengkap = document._get_alamat()

                data["KD_JENIS_TRANSAKSI"] = str(document.enofa_jenis_transaksi)
                data["FG_PENGGANTI"] = document.enofa_fg_pengganti
                data["NOMOR_FAKTUR"] = no_faktur
                data["REFERENSI"] = document.number
                data["MASA_PAJAK"] = document.enofa_masa_pajak
                data["TAHUN_PAJAK"] = document.enofa_tahun_pajak
                data["TANGGAL_FAKTUR"] = document.enofa_tanggal_dokumen
                data["NPWP"] = document.partner_id.commercial_partner_id.vat
                data["NAMA"] = document.partner_id.commercial_partner_id.legal_name
                data["ALAMAT_LENGKAP"] = alamat_lengkap
                data["JUMLAH_DPP"] = document._get_jumlah_dpp(list_code_acc_exceptions)
                data["JUMLAH_PPN"] = document.amount_tax

                header_1_list = ["FK"] + [data[f] for f in header_1[1:]]
                result += _csv_row(header_1_list, delimiter)

                header_2_list = [
                    "FAPR",
                    document.enofa_nama,
                    document.enofa_alamat_lengkap,
                ] + [data[f] for f in header_2[3:]]
                result += _csv_row(header_2_list, delimiter)

                lines = document._prepare_data_detail(list_code_acc_exceptions)
                header_3_list = (
                    ["OF"] + [str(lines[f]) for f in header_3[1:-2]] + ["0", "0"]
                )
                result += _csv_row(header_3_list, delimiter)
        return result

    @api.multi
    def action_generate_efaktur(self, list_code_acc_exceptions):
        obj_ir_attachment = self.env["ir.attachment"]
        if self.filtered(lambda x: x.type != "out_invoice"):
            strWarning = _("Documents are not Customer Invoices")
            raise UserError(strWarning)

        delimiter = ","
        output_head = self._generate_efaktur_invoice(
            delimiter, list_code_acc_exceptions
        )
        my_utf8 = output_head.encode("utf-8")
        datas = base64.b64encode(my_utf8)

        criteria = [("name", "=", "sprint_efaktur.csv")]
        existing_attachment_id = obj_ir_attachment.search(criteria)

        if existing_attachment_id:
            existing_attachment_id.unlink()

        attachment = obj_ir_attachment.create(self._prepare_attachment_data(datas))
        url = "/web/binary/saveas"
        return {
            "type": "ir.actions.act_url",
            "url": url
            + "?model=ir.attachment&field=datas&filename_field=datas_fname&id=%s"
            % (attachment.id),
            "target": "new",
        }

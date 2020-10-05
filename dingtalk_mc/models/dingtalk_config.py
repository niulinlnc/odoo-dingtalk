# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class DingTalkConfig(models.Model):
    _name = 'dingtalk.mc.config'
    _description = "参数配置"
    _rec_name = 'name'

    company_id = fields.Many2one('res.company', string='关联公司', default=lambda self: self.env.user.company_id, index=True)
    name = fields.Char(string='钉钉企业名称', index=True, required=True)
    agent_id = fields.Char(string=u'AgentId')
    corp_id = fields.Char(string=u'CorpId')
    app_key = fields.Char(string=u'AppKey')
    app_secret = fields.Char(string=u'AppSecret')
    login_id = fields.Char(string=u'用于登录AppId')
    login_secret = fields.Char(string=u'用于登录AppSecret')
    m_login = fields.Boolean(string="钉钉免登？", help="开启后允许从钉钉工作台免密码登录到odoo系统。")
    token = fields.Boolean(string="Token")
    delete_is_sy = fields.Boolean(string=u'删除基础数据自动同步?')
    cron_attendance = fields.Boolean(string=u'定时获取考勤数据?')
    not_update_emp_in_hidden_dep = fields.Boolean(string=u'禁止同步隐藏部门的员工.')
    is_auto_create_user = fields.Boolean(string="自动创建系统用户？", default=False,
                                         help='开启自动创建系统用户后，系统将会在收到钉钉回调通知后，立即创建一个属于该员工的系统用户！')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', '钉钉企业名称已存在，请更换！'),
        ('company_id_uniq', 'UNIQUE (company_id)', '该企业对应的公司存在，请更换！'),
    ]

    @api.constrains('m_login')
    def _constrains_login(self):
        """
        由于钉钉免登传递参数原因，无法确认是哪个企业需要进行免登，所以直接在本地指定一个免登企业，但是只有一个
        :return:
        """
        for res in self:
            config_count = self.search_count([('m_login', '=', True)])
            if config_count > 1:
                raise UserError("由于钉钉api原因无法同时开启两个或两个以上的企业免登应用功能。")

    def set_default_user_groups(self):
        """
        设置默认系统用户权限
        :return:
        """
        action = self.env.ref('base.action_res_users').read()[0]
        action['res_id'] = self.env.ref('base.default_user').id
        action['views'] = [[self.env.ref('base.view_users_form').id, 'form']]
        return action

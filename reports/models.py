from django.db import models
from django.utils import timezone

# Create your models here.


class Report(models.Model):
    """体检报告的基本信息"""

    sex_choices = (
        ('boy', '男'),
        ('girl', '女'),
    )

    hospital = models.CharField(max_length=200, verbose_name='医院')
    title = models.CharField(max_length=80, verbose_name='标题', default='20**年报告', unique=True)
    report_num = models.CharField(max_length=20, verbose_name='体检编号', unique=False, blank=False)
    name = models.CharField(max_length=5, verbose_name='姓名')
    sex = models.CharField(choices=sex_choices, max_length=5, verbose_name='性别', default='boy')
    age = models.IntegerField(verbose_name='年龄', blank=False, default='0')
    work_unit = models.CharField(verbose_name='工作单位', max_length=20, default='南京证券吴江营业部')
    date = models.DateTimeField(verbose_name='体检日期', default=timezone.now)

    class Meta:
        ordering = ('-date',)
        verbose_name = '体检报告'
        verbose_name_plural = '体检报告'

    def __str__(self):
        return self.title


class Category(models.Model):
    """某份报告的检查科室"""
    name = models.CharField(max_length=200, verbose_name='科室大类', unique=False)

    class Meta:
        verbose_name_plural = '科室大类'
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.name


class Summary(models.Model):
    """某份报告某个大类的小结"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name='所属报告')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='所属科室')

    content = models.TextField(verbose_name='小结内容')
    doctor = models.CharField(max_length=80, verbose_name='小结医生')

    class Meta:
        verbose_name_plural = '小结'
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.content[:50] + '...'


class Entry(models.Model):
    """具体项目"""
    tips_choice = (
        ('↑', '↑'),
        ('↓', '↓'),
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name='所属报告')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='科室')

    name = models.CharField(max_length=50, verbose_name='项目名称')
    check_results = models.TextField(verbose_name='检查结果')
    unit = models.CharField(max_length=10, verbose_name='单位', blank=True)
    reference_range = models.CharField(max_length=20, verbose_name='参考范围', blank=True)
    tips = models.CharField(choices=tips_choice, max_length=10, verbose_name='提示', blank=True)

    class Meta:
        verbose_name_plural = '检查项目'
        verbose_name = '检查项目'

    def __str__(self):
        return self.name


class Conclusion(models.Model):
    """总检结论"""

    report = models.OneToOneField(Report, verbose_name='所属报告', on_delete=models.CASCADE)

    overview = models.TextField(verbose_name='综述')
    proposal = models.TextField(verbose_name='建议')
    summary_doctor = models.CharField(max_length=5, verbose_name='总检医生')
    summary_date = models.DateTimeField(verbose_name='总检日期', default=timezone.now)

    class Meta:
        verbose_name = '总检结论'
        verbose_name_plural = '总检结论'

    def __str__(self):
        return self.overview[:50] + '...'
